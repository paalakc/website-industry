from pydantic import BaseModel
from typing import List, Optional

class CountryValue(BaseModel):
    country: str
    value_usd: float

class ProductValue(BaseModel):
    hs_code: str
    product_name: str
    value_usd: float

class IndustryValue(BaseModel):
    industry: str
    value_usd: float
    share_pct: float

# 1. Companies
class CompaniesResponse(BaseModel):
    total_unique_exporters: int
    industry_filter: Optional[str]
    year_filter: Optional[int]

# 2. Manufacturers
class ManufacturerEntry(BaseModel):
    rank: int
    country: str
    total_export_value_usd: float

class ManufacturersResponse(BaseModel):
    industry_filter: Optional[str]
    year_filter: Optional[int]
    results: List[ManufacturerEntry]

# 3. Market size
class MarketSizeResponse(BaseModel):
    industry_filter: Optional[str]
    year_filter: Optional[int]
    total_trade_value_usd: float
    trend_by_year: dict

# 4. Export data
class ExportDataResponse(BaseModel):
    exporter: Optional[str]
    industry_filter: Optional[str]
    year_filter: Optional[int]
    top_destinations: List[CountryValue]
    top_products: List[ProductValue]

# 5. Import partners
class ImportPartnersResponse(BaseModel):
    importer: Optional[str]
    industry_filter: Optional[str]
    year_filter: Optional[int]
    top_sources: List[CountryValue]

# 6. End-user industries
class EndIndustriesResponse(BaseModel):
    year_filter: Optional[int]
    industries: List[IndustryValue]