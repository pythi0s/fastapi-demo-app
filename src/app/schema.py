from pydantic import BaseModel
import datetime


class Item(BaseModel):
    name: str
    description: str
    manufacturer: str
    category: str
    price: float
    timestamp: datetime.datetime = datetime.datetime.now().isoformat()
