from pydantic import BaseModel
from typing import Optional

class Specs(BaseModel):
    cpu: Optional[str] = "Not specified"
    ram: Optional[str] = "Not specified"
    storage: Optional[str] = "Not specified"
    ddos_protect: Optional[bool] = False
    
    class Config:
        orm_mode = True
        schema_extra = {
            "specs": {
                "cpu": "Intel Core i9-9900K",
                "ram": "64GB DDR4",
                "storage": "2TB NVMe SSD",
                "ddos_protect": True
            }
        }