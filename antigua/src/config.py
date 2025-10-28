from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "VideoGenerator")
    output_dir : str = os.getenv("OUTPUT_DIR", "./outputs")

settings = Settings()