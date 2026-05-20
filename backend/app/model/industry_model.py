from dataclasses import dataclass
from typing import Optional

@dataclass
class TradeRecord:
    year: int
    exporter_name: str
    importer_name: str
    hs_code: str
    product_name: str
    value: float
    quantity: Optional[float] = 0.0