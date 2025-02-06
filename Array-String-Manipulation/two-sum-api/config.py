# ===================== CONFIGURATION =====================
# config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/twosumdb")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))