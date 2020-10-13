import os

STORAGE_URI = os.getenv("STORAGE_URI", "postgresql+asyncpg://postgres:password@postgresql/postgres")
DEBUG_SQL = int(os.getenv("DEBUG_SQL", "0"))
