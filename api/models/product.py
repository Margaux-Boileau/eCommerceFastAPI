from pydantic import BaseModel
from typing import Optional
from api.models.specs import Specs

class Product(BaseModel):
    id: Optional[str]
    name: str
    image: str
    category: str
    price: float
    location: str
    specs: Optional[Specs] | None = None
    stock: int
    times_bought: int
    
    
