from pydantic import BaseModel
from typing import Optional
from api.models.specs import Specs

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    image: str
    category: str
    price: float
    location: str
    specs: Optional[Specs]  = None
    stock: int
    times_bought: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name" : "Minecraft Server",
                "image": "minecraft.jpg",
                "category": "Game",
                "price": 1.99,
                "location": "Spain",
                "specs": {
                    "cpu": "Intel Core i9-9900K",
                    "ram": "64GB DDR4",
                    "storage": "2TB NVMe SSD",
                    "ddos_protect": True
                },
                "stock": 3,
                "times_bought": 1
            }
        }