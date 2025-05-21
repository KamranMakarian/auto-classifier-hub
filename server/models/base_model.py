from abc import ABC, abstractmethod
from typing import Any, Tuple, List
import pandas as pd

class BaseModel(ABC):
    """
    Abstract base class for all models in the system.
    """

    def __init__(self):
        self.model: Any = None  # Common attribute for subclasses

    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> Tuple[Any, float]:
        """
        Train the model using provided features and target.
        Returns the trained model and an evaluation metric (e.g., accuracy).
        """
        pass

    @abstractmethod
    def predict(self, input_data: List[List[float]]) -> List:
        """
        Predict output using the trained model and new input data.
        Each row in input_data should be a list of feature values.
        """
        pass