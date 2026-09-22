import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_URL = os.getenv("DATABASE_URL")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")
    API_ROOT = os.getenv("API_ROOT", "https://jsonplaceholder.typicode.com")
    ORIGIN = os.getenv(
        "ORIGIN",
        "http://localhost:3000"
    ).split(",")

config = Config()