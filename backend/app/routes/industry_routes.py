from fastapi import APIRouter, Query
from typing import Optional
from app.services.industry_service import (
    get_total_companies,
    get_major_manufacturers,
    get_market_size,
    get_export_data,
    get_import_partners,
    get_end_user_industries,
)
from app.services.processing_service import (
    get_all_countries,
    get_all_industries,
    get_available_years,
    get_top_products,
)

router = APIRouter(prefix="/api/trade", tags=["Trade Data"])


@router.get("/companies")
def companies(
    industry: Optional[str] = Query(None, description="e.g. Automotive"),
    year: Optional[int] = Query(None, description="2018–2024")
):
    return get_total_companies(industry, year)


@router.get("/manufacturers")
def manufacturers(
    industry: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: int = Query(15, le=50)
):
    return get_major_manufacturers(industry, year, limit)


@router.get("/market-size")
def market_size(
    industry: Optional[str] = Query(None),
    year: Optional[int] = Query(None)
):
    return get_market_size(industry, year)


@router.get("/exports")
def export_data(
    exporter: Optional[str] = Query(None, description="e.g. China"),
    industry: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: int = Query(15, le=50)
):
    return get_export_data(exporter, industry, year, limit)


@router.get("/imports")
def import_partners(
    importer: Optional[str] = Query(None, description="e.g. Germany"),
    industry: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: int = Query(15, le=50)
):
    return get_import_partners(importer, industry, year, limit)


@router.get("/end-industries")
def end_industries(year: Optional[int] = Query(None)):
    return get_end_user_industries(year)


@router.get("/countries")
def list_countries():
    return {"countries": get_all_countries()}


@router.get("/industries")
def list_industries():
    return {"industries": get_all_industries()}


@router.get("/years")
def list_years():
    return {"years": get_available_years()}


@router.get("/products")
def top_products(
    year: Optional[int] = Query(None),
    limit: int = Query(20, le=100)
):
    return get_top_products(year, limit)