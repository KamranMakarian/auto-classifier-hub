from config.db import Base, engine
from models.user import User
from models.trained_model import TrainedModel

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")