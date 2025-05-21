from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from models.logistic import LogisticRegressionModel
from models.random_forest import RandomForestModel
from models.neural_net import NeuralNetModel
from models.base_model import BaseModel
from sqlalchemy.orm import Session
from config.settings import SAVED_MODELS_DIR
from services.db_ops import record_model_metadata
from typing import Tuple, Any
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


# Registry maps model names (from frontend) to their classes
model_registry = {
    "logisticregression": LogisticRegressionModel,
    "randomforest": RandomForestModel,
    "neuralnet": NeuralNetModel
}


def train_model(
    model_type: str,
    X: pd.DataFrame,
    y: pd.Series,
    params: dict,
    test_size: float,
    k_fold: int,
    db: Session,
    user_id: int,
    file_name: str
) -> Tuple[Any, float, str]:

    model_type = model_type.lower()
    is_supported_model(model_type)

    model_class = model_registry[model_type]
    model_instance: BaseModel = model_class(params)

    if k_fold > 1:
        from sklearn.base import clone

        if model_type == "logisticregression":
            base_estimator = LogisticRegression(**params)
        elif model_type == "randomforest":
            base_estimator = RandomForestClassifier(**params)
        else:
            base_estimator = model_class(params).model
        scores = cross_val_score(clone(base_estimator), X, y, cv=k_fold)
        mean_acc = float(np.mean(scores))
        model_instance.train(X, y)

        final_file_name = save_model_to_disk(model_instance, file_name, model_type)
        record_model_metadata(db, user_id, file_name, model_type, final_file_name, mean_acc, params)

        return model_instance, mean_acc, final_file_name

    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        y_train = pd.Categorical(y_train).codes.astype(np.int64)
        y_test = pd.Categorical(y_test).codes.astype(np.int64)

        model_instance.train(X_train, y_train)

        y_pred = model_instance.model.predict(X_test)
        if model_type == "neuralnet":
            y_pred = (y_pred > 0.5).astype(int).flatten()

        acc = accuracy_score(y_test, y_pred)
        final_file_name = save_model_to_disk(model_instance, file_name, model_type)
        record_model_metadata(db, user_id, file_name, model_type, final_file_name, acc, params)

        return model_instance, acc, final_file_name


def make_prediction(model: BaseModel,
                    model_name: str,
                    input_data: list,
                    return_proba: bool = False) -> list:

    is_supported_model(model_name)

    if return_proba and hasattr(model.model, "predict_proba"):
        probs = model.model.predict_proba(input_data)
        return probs.tolist()

    return model.predict(input_data)


def save_model_to_disk(model: BaseModel, model_name: str, model_type: str) -> str:
    """
    Saves the model using the provided file_name and correct extension.
    Returns final saved filename.
    """
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    ext = "joblib" if model_type == "logisticregression" or model_type == "randomforest" else "keras"
    final_file_name = f"{model_name}.{ext}"
    save_path = os.path.join(SAVED_MODELS_DIR, final_file_name)

    if ext == "joblib":
        joblib.dump(model.model, save_path)
    else:
        model.model.save(save_path)

    print(f"[INFO] Model saved to: {save_path}")
    return final_file_name


def load_model_from_disk(model_type: str, file_name: str) -> BaseModel:
    is_supported_model(model_type.lower())

    model_class = model_registry[model_type.lower()]
    model_instance: BaseModel = model_class()

    path = os.path.join(SAVED_MODELS_DIR, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"No saved model found at {path}")

    if file_name.endswith(".joblib"):
        model_instance.model = joblib.load(path)
    elif file_name.endswith(".keras"):
        from tensorflow.keras.models import load_model
        model_instance.model = load_model(path)
    else:
        raise ValueError(f"Unsupported file extension in {file_name}")

    return model_instance


def is_supported_model(model_name: str):
    if model_name not in model_registry:
        raise ValueError(f"Unsupported model: {model_name}")


