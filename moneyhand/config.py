import os
from pathlib import Path

STORAGE_URI = os.getenv("STORAGE_URI", "postgres:password@postgresql/postgres")
DEBUG_SQL = int(os.getenv("DEBUG_SQL", "0"))


BASE_DIR = Path(__file__).absolute().parent
