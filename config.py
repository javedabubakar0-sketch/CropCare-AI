"""
CropCare AI - Configuration Module
Centralizes application settings, security constraints, filesystem directories,
and environment variable overrides.
"""

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Security & Secrets
SECRET_KEY = os.getenv("SECRET_KEY", "cropcare-secret-key-bscs-2026")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# Environment Detection (Vercel / AWS Lambda Serverless)
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

# Storage Folders
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
SAMPLES_FOLDER = os.path.join(STATIC_FOLDER, "sample_leaves")
MODELS_FOLDER = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_FOLDER, "plant_disease_model.joblib")
CLASSES_PATH = os.path.join(MODELS_FOLDER, "classes.json")

if IS_VERCEL:
    # Serverless runtime: only /tmp is writable
    UPLOAD_FOLDER = os.path.join("/tmp", "uploads")
    DB_PATH = os.getenv("DATABASE_PATH", os.path.join("/tmp", "cropcare.db"))
    
    # Copy pre-seeded SQLite database to /tmp so it is fully writable
    src_db = os.path.join(BASE_DIR, "cropcare.db")
    if not os.path.exists(DB_PATH) and os.path.exists(src_db):
        try:
            import shutil
            shutil.copy2(src_db, DB_PATH)
        except Exception:
            pass
else:
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads")
    DB_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "cropcare.db"))

# Ensure required runtime directories exist safely (prevent crash on read-only serverless filesystems)
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(SAMPLES_FOLDER, exist_ok=True)
    os.makedirs(MODELS_FOLDER, exist_ok=True)
except OSError:
    pass

# Upload Constraints (Security)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB maximum upload
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

# Weather Service Configuration
WEATHER_CACHE_TTL_SECONDS = 600  # 10 minutes cache
WEATHER_REQUEST_TIMEOUT = 6      # 6 seconds timeout for external API requests

# Application Metadata
APP_NAME = "CropCare AI"
APP_VERSION = "2.0.0"
