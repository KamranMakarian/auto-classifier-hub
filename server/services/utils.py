from fastapi import HTTPException

def ensure_model_loaded():
    if trained_model is None:
        raise HTTPException(status_code=400, detail="No model is currently loaded or trained.")
