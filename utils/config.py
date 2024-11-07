# utils/config.py
from dotenv import load_dotenv
import os
from pathlib import Path

def load_config():
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(dotenv_path=project_root / ".env")

    config = {
        "username": os.getenv("LOGIN_USERNAME"),
        "password": os.getenv("LOGIN_PASSWORD"),
        "base_url": os.getenv("BASE_URL"),
    }
    return config
