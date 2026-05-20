from typing import Optional
from app.services.processing_service import get_filtered_df
from app.schemas.industry_schema import (
    CompaniesResponse, ManufacturersResponse, ManufacturerEntry,
    MarketSizeResponse, ExportDataResponse, ImportPartnersResponse,
    EndIndustriesResponse, CountryValue, ProductValue, IndustryValue
)
from app.utils.hs_industry_map import get_industry_from_hs


# 1. TOTAL COMPANIES
def get_total_companies(
    industry: Optional[str] = None,
    year: Optional[int] = None
) -> CompaniesResponse:
    df = get_filtered_df(year=year, industry=industry)
    return CompaniesResponse(
        total_unique_exporters=int(df["exporter_name"].nunique()),
        industry_filter=industry,
        year_filter=year
    )


# 2. MAJOR MANUFACTURERS
def get_major_manufacturers(
    industry: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = 15
) -> ManufacturersResponse:
    df = get_filtered_df(year=year, industry=industry)
    ranked = (
        df.groupby("exporter_name")["value"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )
    results = [
        ManufacturerEntry(
            rank=i + 1,
            country=country,
            total_export_value_usd=round(float(val), 2)
        )
        for i, (country, val) in enumerate(ranked.items())
    ]
    return ManufacturersResponse(
        industry_filter=industry,
        year_filter=year,
        results=results
    )


# 3. MARKET SIZE
def get_market_size(
    industry: Optional[str] = None,
    year: Optional[int] = None
) -> MarketSizeResponse:
    df = get_filtered_df(year=year, industry=industry)
    total = round(float(df["value"].sum()), 2)
    trend = df.groupby("year")["value"].sum().sort_index()
    return MarketSizeResponse(
        industry_filter=industry,
        year_filter=year,
        total_trade_value_usd=total,
        trend_by_year={int(k): round(float(v), 2) for k, v in trend.items()}
    )


# 4. EXPORT DATA
def get_export_data(
    exporter: Optional[str] = None,
    industry: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = 15
) -> ExportDataResponse:
    df = get_filtered_df(year=year, industry=industry, exporter=exporter)

    top_dest = (
        df.groupby("importer_name")["value"]
        .sum().sort_values(ascending=False).head(limit)
    )
    destinations = [
        CountryValue(country=k, value_usd=round(float(v), 2))
        for k, v in top_dest.items()
    ]

    top_prod = (
        df.groupby(["hs_code", "product_name"])["value"]
        .sum().sort_values(ascending=False).head(limit)
    )
    products = [
        ProductValue(
            hs_code=idx[0],
            product_name=idx[1],
            value_usd=round(float(v), 2)
        )
        for idx, v in top_prod.items()
    ]

    return ExportDataResponse(
        exporter=exporter,
        industry_filter=industry,
        year_filter=year,
        top_destinations=destinations,
        top_products=products
    )


# 5. IMPORT PARTNERS
def get_import_partners(
    importer: Optional[str] = None,
    industry: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = 15
) -> ImportPartnersResponse:
    df = get_filtered_df(year=year, industry=industry, importer=importer)
    top_sources = (
        df.groupby("exporter_name")["value"]
        .sum().sort_values(ascending=False).head(limit)
    )
    sources = [
        CountryValue(country=k, value_usd=round(float(v), 2))
        for k, v in top_sources.items()
    ]
    return ImportPartnersResponse(
        importer=importer,
        industry_filter=industry,
        year_filter=year,
        top_sources=sources
    )


# 6. END-USER INDUSTRIES
def get_end_user_industries(
    year: Optional[int] = None
) -> EndIndustriesResponse:
    df = get_filtered_df(year=year)
    df = df.copy()
    df["industry"] = df["hs_code"].apply(get_industry_from_hs)
    grouped = df.groupby("industry")["value"].sum().sort_values(ascending=False)
    total = grouped.sum()
    industries = [
        IndustryValue(
            industry=k,
            value_usd=round(float(v), 2),
            share_pct=round(float(v / total) * 100, 2)
        )
        for k, v in grouped.items()
    ]
    return EndIndustriesResponse(year_filter=year, industries=industries)