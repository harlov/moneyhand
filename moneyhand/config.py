import os
from pathlib import Path
import logging
from uuid import UUID


def convert_to_bool(v):
    if isinstance(v, bool):
        return v

    _v = v.lower()
    if _v in {"0", "false", "f"}:
        return False
    if _v in {"1", "true", "t"}:
        return True

    return None


# Common settings
BASE_DIR = Path(__file__).absolute().parent
DEBUG = convert_to_bool(os.getenv("DEBUG", "0"))
LOG_LEVEL = logging.getLevelName(os.getenv("LOG_LEVEL", "WARNING"))

# Database
STORAGE_URI = os.getenv("STORAGE_URI")
DEBUG_SQL = int(os.getenv("DEBUG_SQL", DEBUG))

# Default tenant variables
DEFAULT_TENANT_UUID = UUID(
    os.getenv("DEFAULT_TENANT_UUID", "00000000-0000-0000-0000-000000000000")
)
DEFAULT_TENANT_USER = os.getenv("DEFAULT_TENANT_USER", "admin")
DEFAULT_TENANT_PASSWORD = os.getenv("DEFAULT_TENANT_PASSWORD", "password")
DEFAULT_TENANT_EMAIL = os.getenv("DEFAULT_TENANT_EMAIL", "admin@test.local")

# Security
HASH_SECRET_KEY = os.getenv("HASH_SECRET_KEY", "VERYSECRETKEY")  # openssl rand -hex 32
USER_TOKEN_LIFETIME_SEC = int(os.getenv("USER_TOKEN_LIFETIME_SEC", 600))


# REST interface
API_DEBUG = convert_to_bool(os.getenv("DEBUG_API", DEBUG))
API_ROOT_PATH = os.getenv("API_ROOT_PATH", "")

# Telegram interface
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", None)
TELEGRAM_GOD_USER = os.getenv("TELEGRAM_GOD_USER", None)
