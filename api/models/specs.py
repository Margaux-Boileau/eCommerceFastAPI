from pydantic import BaseModel
from typing import Optional

class Specs(BaseModel):
    cpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    ddos_protect: Optional[bool] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "specs": {
                "cpu": "Intel Core i9-9900K",
                "ram": "64GB DDR4",
                "storage": "2TB NVMe SSD",
                "ddos_protect": True
            }
        }