from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Optional default

    class Config:
        env_file = ".env"

settings = Settings()

SAVED_MODELS_DIR = "saved_models" # directory where models will be saved after training.
MAX_BATCH_SIZE = 500 # sets the maximum number of samples that can be accepted as input for prediction.
