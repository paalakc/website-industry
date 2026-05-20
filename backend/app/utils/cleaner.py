import pandas as pd

COLUMN_RENAME_MAP = {
    "year":           "year",
    "exporter_name":  "exporter_name",
    "exporter _name": "exporter_name",
    "importer_name":  "importer_name",
    "importer _name": "importer_name",
    "hs_code":        "hs_code",
    "product_name":   "product_name",
    "value":          "value",
    "quantity":       "quantity",
}

FINAL_COLUMNS = [
    "year",
    "exporter_name",
    "importer_name",
    "hs_code",
    "product_name",
    "value",
    "quantity",
]

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    # Step 1: normalize column names
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns=COLUMN_RENAME_MAP)

    # Step 2: keep only needed columns
    available = [c for c in FINAL_COLUMNS if c in df.columns]
    missing   = [c for c in FINAL_COLUMNS if c not in df.columns]
    if missing:
        print(f"  Warning — missing columns: {missing}")
    df = df[available].copy()

    # Step 3: fix data types before null checks
    df["value"]    = pd.to_numeric(df["value"],    errors="coerce")
    df["year"]     = pd.to_numeric(df["year"],     errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["hs_code"]  = df["hs_code"].astype(str).str.strip().str.zfill(6)

    # Step 4: drop rows missing critical fields
    df = df.dropna(subset=["exporter_name", "importer_name", "value", "year", "hs_code"])

    # Step 5: fill non-critical nulls with defaults
    df["product_name"] = df["product_name"].fillna("Unknown Product")
    df["quantity"]     = df["quantity"].fillna(0)

    # Step 6: remove bad data
    df = df[df["value"] > 0]
    df = df[df["year"].between(2018, 2024)]

    # Step 7: normalize strings
    for col in ["exporter_name", "importer_name", "product_name"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # Step 8: drop duplicates
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    # Step 9: shrink data types to reduce memory
    df["value"]    = df["value"].astype("float32")
    df["quantity"] = df["quantity"].astype("float32")
    df["year"]     = df["year"].astype("int16")

    return df