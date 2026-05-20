import pandas as pd
from pathlib import Path
from app.utils.cleaner import clean_dataframe

def load_csv_file(filepath: Path) -> pd.DataFrame:
    """Load and clean a single CSV file."""
    df = pd.read_csv(filepath, low_memory=False)
    df = clean_dataframe(df)
    return df

def load_all_csvs(datasets_dir: Path) -> pd.DataFrame:
    """Load, clean and merge all CSV files from the Datasets folder."""
    all_files = sorted(datasets_dir.glob("*.csv"))
    if not all_files:
        raise RuntimeError(f"No CSV files found in {datasets_dir}")

    frames = []
    for f in all_files:
        try:
            df = load_csv_file(f)
            frames.append(df)
            print(f"✓ {f.name}: {len(df):,} rows")
        except Exception as e:
            print(f"✗ Skipping {f.name} — {e}")

    if not frames:
        raise RuntimeError("All CSV files failed to load.")

    combined = pd.concat(frames, ignore_index=True)

    # Final dedup across files (OEC files can overlap between years)
    combined = combined.drop_duplicates().reset_index(drop=True)

    mem_mb = combined.memory_usage(deep=True).sum() / 1e6
    print(f"\n✓ Total: {len(combined):,} rows | Memory: {mem_mb:.1f} MB")

    return combined