from pydantic import BaseModel
from typing import List, Optional

class PredictRequest(BaseModel):
    """
    Schema for batch prediction input.
    
    Attributes:
    - input_data: A list of feature vectors (2D list of floats)
    - return_proba: Whether to return class probabilities (optional)
    """
    input_data: List[List[float]]
    return_proba: Optional[bool] = False
