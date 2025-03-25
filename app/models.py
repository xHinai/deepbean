from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GreenBean(BaseModel):
    bean_id: Optional[str] = None
    name: str
    origin: Optional[str] = None
    processing: Optional[str] = None
    variety: Optional[str] = None
    altitude: Optional[str] = None
    purchase_date: Optional[str] = None
    initial_stock_kg: Optional[float] = None
    current_stock_kg: Optional[float] = None
    price_per_kg: Optional[float] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None

class CoffeeRoast(BaseModel):
    roast_id: Optional[str] = None
    bean_id: Optional[str] = None  # Add this field to link to green beans
    date: Optional[str] = None
    coffee_name: str
    agtron_whole: Optional[int] = None
    agtron_ground: Optional[int] = None
    drop_temp: Optional[float] = None
    development_time: Optional[float] = None
    total_time: Optional[float] = None
    dtr_ratio: Optional[float] = None
    notes: Optional[str] = None

class CoffeeScore(BaseModel):
    score_id: str
    roast_id: str  # Foreign key to link to roast
    date: datetime
    fragrance_aroma: float
    flavor: float
    aftertaste: float
    acidity: float
    body: float
    uniformity: float
    clean_cup: float
    sweetness: float
    overall: float
    defects: int
    total_score: float
    notes: Optional[str] = None 