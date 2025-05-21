from fastapi import FastAPI, UploadFile, File, Form, Query, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.request_response import PredictRequest
from services.trainer import train_model, make_prediction
from services.trainer import load_model_from_disk
from utils.data import load_csv_data
from models.trained_model import TrainedModel
import json
import os
from config.settings import SAVED_MODELS_DIR, MAX_BATCH_SIZE
from config.db import SessionLocal, get_db
from routes import auth
from routes.auth import router as auth_router
from dependencies.auth_dependencies import get_current_user
from models.user import User
from fastapi.openapi.utils import get_openapi
import re
from typing import Any
from datetime import datetime
from routes.admin import router as admin_router



app = FastAPI()
app.include_router(auth_router, tags=["Auth"])
app.include_router(admin_router)

# Enable CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (for demo purposes)
trained_model = None
current_model_name = None
target_column = None


@app.post("/fit/", tags=["Training"])
async def fit_model(
    file: UploadFile = File(...),
    model_type: str = Form(...),    
    file_name: str = Form(""),      # Optional custom name
    target: str = Form(...),        
    test_size: float = Form(0.2),
    k_folds: int = Form(0),         # 0 = no K-Fold CV
    params: str = Form("{}"),       
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Train a machine learning model using uploaded CSV data.

    Supports Logistic Regression, Random Forest, and a simple Neural Net.
    Allows for custom hyperparameters, train/test split, and optional K-Fold validation.
    
    Returns:
    - Training accuracy
    - Saved model file name
    """

    global trained_model, current_model_name, current_model_type, target_column

    # Generate default file_name if not provided
    if not file_name:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_name = f"{model_type}_{current_user.id}_{timestamp}"

    df = await load_csv_data(file)
    if target not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target column '{target}' not found in dataset.")

    target_column = target
    current_model_name = file_name

    X = df.drop(columns=[target])
    y = df[target]

    try:
        hyperparams = json.loads(params) if isinstance(params, str) else params
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'params'")

    try:
        trained_model, acc, saved_file_name = train_model(
            model_type=model_type.strip().lower(),
            X=X,
            y=y,
            params=hyperparams,
            test_size=test_size,
            k_fold=k_folds,
            db=db,
            user_id=current_user.id,
            file_name=file_name
        )
        current_model_type = model_type.strip().lower()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

    return {
        "accuracy": acc,
        "file_name": saved_file_name
    }


@app.post("/predict/", tags=["Prediction"])
def predict(
    request: PredictRequest,
    current_user: User = Depends(get_current_user)
):
    ensure_model_loaded()

    if len(request.input_data) > MAX_BATCH_SIZE:
        raise HTTPException(status_code=400, detail=f"Batch too large. Max allowed is {MAX_BATCH_SIZE} samples.")

    prediction = make_prediction(
        trained_model, current_model_type, request.input_data, request.return_proba
    )

    if request.return_proba:
        return {
            "file_name": current_model_name,
            "probabilities": [
                {"index": i, "scores": row} for i, row in enumerate(prediction)
            ]
        }

    return {
        "file_name": current_model_name,
        "predictions": [
            {"index": i, "value": val} for i, val in enumerate(prediction)
        ]
    }




@app.post("/predict-file/", tags=["Prediction"])
async def predict_from_file(
    file: UploadFile = File(...),
    return_proba: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Predict using a trained model by uploading a CSV file with feature rows.

    - The file should contain **only the feature columns** (no target column).
    - The **first row must include feature names** (i.e., the CSV must have a header row).
    - Returns a list of predicted values or class probabilities.
    """

    ensure_model_loaded()

    df = await load_csv_data(file)

    if len(df) > MAX_BATCH_SIZE:
        raise HTTPException(status_code=400, detail=f"Batch too large. Max allowed is {MAX_BATCH_SIZE} rows.")

    input_data = df.values.tolist()

    prediction = make_prediction(
        trained_model, current_model_type, input_data, return_proba
    )

    if return_proba:
        return {
            "file_name": current_model_name,
            "probabilities": [
                {"index": i, "scores": row} for i, row in enumerate(prediction)
            ],
            "rows_predicted": len(prediction)
        }

    return {
        "file_name": current_model_name,
        "predictions": [
            {"index": i, "value": val} for i, val in enumerate(prediction)
        ],
        "rows_predicted": len(prediction)
    }

@app.get("/list-models/", tags=["Model Management"])
def list_saved_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if not os.path.exists(SAVED_MODELS_DIR):
        return {"models": []}

    try:
        if getattr(current_user, "role", None) == "admin":
            models = db.query(TrainedModel).all()
        else:
            models = db.query(TrainedModel).filter(TrainedModel.user_id == current_user.id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query models: {str(e)}")

    return {
        "models": [
            {
                "id": m.id,
                "user_id": m.user_id,
                "name": m.name,
                "model_type": m.model_type,
                "accuracy": m.accuracy,
                "file_path": m.file_path,
                "created_at": m.created_at,
            } for m in models
        ]

    }


@app.post("/load-model/", tags=["Model Management"])
def load_model(
    file_name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Load a previously saved model by file name (e.g., 'RandomForest_latest').

    The model must exist in the saved_models folder. 
    """
    global trained_model, current_model_name, current_model_type

    # Fetch metadata for the model
    model_record = db.query(TrainedModel).filter_by(name=file_name).first()

    if not model_record:
        raise HTTPException(status_code=404, detail="Model metadata not found in DB")

    if model_record.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have access to this model.")

    try:
        trained_model = load_model_from_disk(
            model_type=model_record.model_type, 
            file_name=os.path.basename(model_record.file_path)
        )
        current_model_name = model_record.name
        current_model_type = model_record.model_type
        return {"message": f"Model '{file_name}' loaded successfully."}
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"error": f"No saved model file found for '{file_name}'."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    
@app.delete("/delete-model/", tags=["Model Management"])
def delete_model(
    file_name: str = Query(..., description="Name of the saved model file"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    model_path = os.path.join(SAVED_MODELS_DIR, file_name)

    if not is_valid_filename(file_name):
        return JSONResponse(status_code=400, content={"error": "Invalid filename."})

    model_record = db.query(TrainedModel).filter(TrainedModel.file_path == model_path).first()

    if not model_record:
        return JSONResponse(status_code=404, content={"error": "Model metadata not found in DB."})

    if model_record.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this model.")

    if not os.path.exists(model_path):
        return JSONResponse(status_code=404, content={"error": f"File '{model_path}' not found."})

    try:
        os.remove(model_path)
        db.delete(model_record)
        db.commit()
        return {"message": f"Model file '{file_name}' deleted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.delete("/delete-all-models/", tags=["Model Management"])
def delete_all_models(
    confirm: bool = Query(False, description="Set to true to confirm deletion"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not confirm:
        return JSONResponse(
            status_code=400, 
            content={"error": "Confirmation required. Set ?confirm=true to proceed."}
        )

    deleted_files = []
    failed_deletions = []

    try:
        if current_user.role == "admin":
            models = db.query(TrainedModel).all()
        else:
            models = db.query(TrainedModel).filter_by(user_id=current_user.id).all()

        for model in models:
            try:
                file_path = os.path.normpath(model.file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(model.name)
                db.delete(model)
            except Exception as e:
                failed_deletions.append({"file": model.name, "error": str(e)})

        db.commit()

        return {
            "message": f"Deleted {len(deleted_files)} model file(s).",
            "deleted_files": deleted_files,
            "failed": failed_deletions
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.put("/rename-model/", tags=["Model Management"])
def rename_model(
    current_name: str = Form(..., description="Current logical model name (no extension)"),
    new_name: str = Form(..., description="New logical model name (no extension)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Rename a trained model: updates both the logical name in the DB
    and the actual filename on disk.

    Both `current_name` and `new_name` should NOT include file extensions.
    """

    # Fetch existing model
    model_record = db.query(TrainedModel).filter_by(name=current_name).first()

    if not model_record:
        raise HTTPException(status_code=404, detail="Model not found in database.")

    if model_record.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to rename this model.")

    # Extract the current file extension
    old_path = model_record.file_path
    _, ext = os.path.splitext(old_path)
    ext = ext.lstrip(".")  # remove the dot

    old_file_path = os.path.join(SAVED_MODELS_DIR, f"{current_name}.{ext}")
    new_file_path = os.path.join(SAVED_MODELS_DIR, f"{new_name}.{ext}")

    # Check if new name already exists (logical or physical)
    if db.query(TrainedModel).filter_by(name=new_name).first():
        raise HTTPException(status_code=400, detail="A model with the new name already exists in the database.")

    if os.path.exists(new_file_path):
        raise HTTPException(status_code=400, detail="A file with the new name already exists on disk.")

    try:
        os.rename(old_file_path, new_file_path)
        model_record.name = new_name
        model_record.file_path = new_file_path
        db.commit()
        db.refresh(model_record)
        return {"message": f"Model renamed to '{new_name}' successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rename model: {str(e)}")

@app.get("/model-metadata/", tags=["Model Management"])
def get_model_metadata(
    file_name: str = Query(..., description="Logical name of the model (no extension)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve detailed metadata about a trained model.

    Requires the logical model name (excluding the file extension).
    """

    model_record = db.query(TrainedModel).filter_by(name=file_name).first()

    if not model_record:
        raise HTTPException(status_code=404, detail="Model metadata not found in the database.")

    if model_record.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have access to this model.")

    return {
        "id": model_record.id,
        "user_id": model_record.user_id,
        "name": model_record.name,
        "model_type": model_record.model_type,
        "accuracy": model_record.accuracy,
        "parameters": model_record.parameters,
        "file_path": model_record.file_path,
        "created_at": model_record.created_at,
    }

def is_valid_filename(file_name: str) -> bool:
    return re.fullmatch(r"[\w\-. ]+\.(joblib|keras)", file_name or "", re.IGNORECASE) is not None

def ensure_model_loaded():
    if trained_model is None or current_model_name is None:
        raise HTTPException(status_code=400, detail="Model not trained or loaded yet")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ML Model API",
        version="1.0.0",
        description="ML Model API with Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
