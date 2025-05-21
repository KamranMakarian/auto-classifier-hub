from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from models.base_model import BaseModel
import pandas as pd
from typing import Any, Tuple, List


class LogisticRegressionModel(BaseModel):
    """
    Concrete implementation of BaseModel for Logistic Regression.
    """

    def __init__(self, params: dict = None):
        """
        Initialize the model with optional hyperparameters.
        """
        self.params = params or {}
        self.model = None

    def train(self, X: pd.DataFrame, y: pd.Series) -> Tuple[Any, float]:
        """
        Train the Logistic Regression model.

        Returns:
        - Trained model
        - Accuracy score on training data
        """
        self.model = LogisticRegression(**self.params)
        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        acc = accuracy_score(y, y_pred)

        return self.model, acc

    def predict(self, input_data: List[List[float]]) -> List:
        """
        Predict using the trained model.

        Parameters:
        - input_data: List of feature vectors (2D list)

        Returns:
        - List of predicted class labels
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")

        return self.model.predict(input_data).tolist()
