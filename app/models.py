from pydantic import BaseModel
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
    bean_id: Optional[str] = None  # Link to green beans
    date: Optional[str] = None
    coffee_name: str
    agtron_whole: Optional[int] = None
    agtron_ground: Optional[int] = None
    drop_temp: Optional[float] = None
    development_time: Optional[float] = None
    total_time: Optional[float] = None
    dtr_ratio: Optional[float] = None
    amount_used_kg: Optional[float] = None  # Amount of green beans used
    notes: Optional[str] = None

class CoffeeScore(BaseModel):
    score_id: Optional[str] = None
    roast_id: str
    date: Optional[str] = None
    fragrance_aroma: Optional[float] = None
    flavor: Optional[float] = None
    aftertaste: Optional[float] = None
    acidity: Optional[float] = None
    body: Optional[float] = None
    uniformity: Optional[float] = None
    clean_cup: Optional[float] = None
    sweetness: Optional[float] = None
    overall: Optional[float] = None
    defects: Optional[int] = None
    total_score: Optional[float] = None
    notes: Optional[str] = None 