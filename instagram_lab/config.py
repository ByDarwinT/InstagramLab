"""Rutas y credenciales centralizadas, independientes del directorio de ejecución."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
PRIMARY_USER = os.getenv("INSTAGRAM_USERNAME")
PRIMARY_PASS = os.getenv("INSTAGRAM_PASSWORD")
BACKUP_USER = os.getenv("INSTAGRAM_USERNAME_BACKUP")
BACKUP_PASS = os.getenv("INSTAGRAM_PASSWORD_BACKUP")
SESSION_FILE = BASE_DIR / "cookies.json"
RESULTS_DIR = BASE_DIR / "output"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
