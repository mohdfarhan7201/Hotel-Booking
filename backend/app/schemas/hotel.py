from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class RoomBase(BaseModel):
    type: str
    description: Optional[str] = None
    price_per_night: float
    capacity: int
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_available: bool = True

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    hotel_id: int

    class Config:
        from_attributes = True

class HotelBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    country: str
    stars: int = 1
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int
    rating: float
    created_at: datetime
    rooms: List[RoomResponse] = []

    class Config:
        from_attributes = True
