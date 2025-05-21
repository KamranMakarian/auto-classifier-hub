from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from models.base_model import BaseModel
import pandas as pd
from typing import Any, Tuple, List


class RandomForestModel(BaseModel):
    """
    Concrete implementation of BaseModel for Random Forest Classifier.
    """

    def __init__(self, params: dict = None):
        """
        Initialize the model with optional hyperparameters.
        """
        self.params = params or {}
        self.model = None 

    def train(self, X: pd.DataFrame, y: pd.Series) -> Tuple[Any, float]:
        """
        Train the Random Forest Classifier.

        Returns:
        - The trained model
        - Accuracy score on training data (for MVP simplicity)
        """
        self.model = RandomForestClassifier(**self.params)
        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        training_accuracy = accuracy_score(y, y_pred)

        return self.model, training_accuracy

    def predict(self, input_data: List[List[float]]) -> List:
        """
        Predict using the trained Random Forest model.

        Parameters:
        - input_data: List of feature vectors (2D list)

        Returns:
        - List of predicted class labels
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")

        return self.model.predict(input_data).tolist()
