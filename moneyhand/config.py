import os
from pathlib import Path
import logging

STORAGE_URI = os.getenv("STORAGE_URI", "postgres:password@postgresql/postgres")
DEBUG_SQL = int(os.getenv("DEBUG_SQL", "0"))
LOG_LEVEL = logging.getLevelName(os.getenv("LOG_LEVEL", "WARNING"))


BASE_DIR = Path(__file__).absolute().parent

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", None)
