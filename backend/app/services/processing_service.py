import pandas as pd
from typing import Optional
from database import load_all_data
from app.utils.hs_industry_map import get_industry_from_hs
from app.utils.formatter import format_value, format_trend, format_rank_list

def get_filtered_df(
    year: Optional[int] = None,
    industry: Optional[str] = None,
    exporter: Optional[str] = None,
    importer: Optional[str] = None,
) -> pd.DataFrame:
    df = load_all_data().copy()

    if year:
        df = df[df["year"] == year]
    if industry:
        df["_industry"] = df["hs_code"].apply(get_industry_from_hs)
        df = df[df["_industry"].str.lower() == industry.lower()]
        df = df.drop(columns=["_industry"])
    if exporter:
        df = df[df["exporter_name"].str.lower() == exporter.lower()]
    if importer:
        df = df[df["importer_name"].str.lower() == importer.lower()]

    return df


def get_all_countries() -> list:
    df = load_all_data()
    exporters = set(df["exporter_name"].dropna().unique())
    importers = set(df["importer_name"].dropna().unique())
    return sorted(exporters | importers)


def get_all_industries() -> list:
    df = load_all_data()
    industries = df["hs_code"].apply(get_industry_from_hs).unique()
    return sorted(set(industries))


def get_available_years() -> list:
    df = load_all_data()
    return sorted([int(y) for y in df["year"].dropna().unique()])


def get_top_products(year: Optional[int] = None, limit: int = 20) -> list:
    df = get_filtered_df(year=year)
    result = (
        df.groupby(["hs_code", "product_name"])["value"]
        .sum().sort_values(ascending=False).head(limit)
    )
    return [
        {
            "hs_code": idx[0],
            "product_name": idx[1],
            "total_value_usd": format_value(v)
        }
        for idx, v in result.items()
    ]