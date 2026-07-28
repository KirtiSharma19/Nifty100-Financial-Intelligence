from pathlib import Path

# Root Project Directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Data Directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Database Directory
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "nifty100.db"

# Export Directory
EXPORT_DIR = BASE_DIR / "exports"

# Assets Directory
ASSETS_DIR = BASE_DIR / "assets"

# Create required folders automatically
DATABASE_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)