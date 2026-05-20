import pandas as pd
from pathlib import Path
from config import DATASETS_DIR, BASE_DIR
from app.utils.csv_loader import load_all_csvs

_df_cache = None
CACHE_FILE = BASE_DIR / "cache.parquet"

def load_all_data() -> pd.DataFrame:
    global _df_cache

    # Already loaded in memory — return instantly
    if _df_cache is not None:
        return _df_cache

    # Parquet cache exists — load it (10x faster than CSVs)
    if CACHE_FILE.exists():
        print("Loading from cache file...")
        _df_cache = pd.read_parquet(CACHE_FILE)
        print(f"✓ Loaded {len(_df_cache):,} rows from cache | Memory: {_df_cache.memory_usage(deep=True).sum() / 1e6:.1f} MB")
        return _df_cache

    # First time — load all CSVs, clean, then save cache
    print("First run — loading from CSVs (this will take a few minutes)...")
    _df_cache = load_all_csvs(DATASETS_DIR)

    print("Saving cache for next time...")
    _df_cache.to_parquet(CACHE_FILE, index=False)
    print("✓ Cache saved — next startup will be instant!")

    return _df_cache