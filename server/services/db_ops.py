from sqlalchemy.orm import Session
from models.trained_model import TrainedModel
from config.settings import SAVED_MODELS_DIR
import os

def record_model_metadata(
    db: Session,
    user_id: int,
    file_name: str,
    model_type: str,
    saved_file_name: str,  # includes .joblib or .keras
    acc: float,
    params: dict
):
    new_model = TrainedModel(
        user_id=user_id,
        name=file_name,  # logical name entered by the user
        model_type=model_type.lower(),
        accuracy=acc,
        parameters=params,
        file_path=os.path.join(SAVED_MODELS_DIR, saved_file_name)
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

