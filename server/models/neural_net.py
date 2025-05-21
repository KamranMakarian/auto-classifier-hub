from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
from models.base_model import BaseModel
import pandas as pd
from typing import Any, Tuple, List
import numpy as np


class NeuralNetModel(BaseModel):
    """
    Simple binary classification neural network using Keras.
    """

    def __init__(self, params: dict = None):
        self.params = params or {}
        self.model = None

    def train(self, X: pd.DataFrame, y: pd.Series) -> Tuple[Any, float]:
        """
        Train a binary classification neural network.
        Returns the trained model and accuracy.
        """
        # Convert input features and labels
        X = X.astype(np.float32)
        y = pd.Categorical(y).codes.astype(np.int64)

        # Confirm only binary classification
        unique_labels = np.unique(y)
        if len(unique_labels) != 2:
            raise ValueError(f"Binary classification only: found {len(unique_labels)} unique classes.")

        # Extract hyperparameters
        activation = self.params.get("activation", "relu")
        hidden_layers = self.params.get("hidden_layer_sizes", [64, 64])
        epochs = self.params.get("epochs", 20)
        batch_size = self.params.get("batch_size", 32)

        # Build model
        model = Sequential()
        model.add(Dense(hidden_layers[0], activation=activation, input_dim=X.shape[1]))
        for units in hidden_layers[1:]:
            model.add(Dense(units, activation=activation))
        model.add(Dense(1, activation="sigmoid"))

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

        self.model = model

        # Predict
        y_pred = self.model.predict(X, verbose=0)

        # Assertions for debugging
        assert y_pred.ndim == 2 and y_pred.shape[1] == 1, f"Unexpected y_pred shape: {y_pred.shape}"
        assert not np.isnan(y_pred).any(), "NaNs found in y_pred"
        assert not np.isinf(y_pred).any(), "Infs found in y_pred"

        y_pred_labels = (y_pred > 0.5).astype(np.int64).flatten()

        # More assertions
        assert y.shape == y_pred_labels.shape, f"Shape mismatch: y {y.shape}, y_pred {y_pred_labels.shape}"
        assert y.dtype == y_pred_labels.dtype, f"Dtype mismatch: y {y.dtype}, y_pred {y_pred_labels.dtype}"

        acc = accuracy_score(y, y_pred_labels)
        return self.model, acc

    def predict(self, input_data: List[List[float]]) -> List[int]:
        """
        Predict class labels for binary classification.
        """
        if self.model is None:
            raise ValueError("Model not trained.")

        input_array = np.array(input_data, dtype=np.float32)
        output = self.model.predict(input_array, verbose=0)
        return np.round(output).astype(int).flatten().tolist()
