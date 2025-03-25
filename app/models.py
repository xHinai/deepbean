from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CoffeeRoast(BaseModel):
    roast_id: str
    date: datetime
    coffee_name: str
    agtron_whole: int
    agtron_ground: int
    drop_temp: Optional[float] = Field(None, description="Drop temperature in °C")
    development_time: float
    total_time: float
    dtr_ratio: float
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