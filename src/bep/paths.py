from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

# The export downloaded manually from the ReBayesed app.
EXPORT_FILE = DATA_DIR / "Individual_Studies" / "filtered-network-data-2026-09-21.rds"

# Files mirrored from the paper's OSF project, under their OSF paths.
OSF_DIR = DATA_DIR / "osf"

# The export as parquet tables, written by bep/tables.py
TABLES_DIR = DATA_DIR / "tables"
