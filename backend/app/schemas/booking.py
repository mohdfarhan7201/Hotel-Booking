from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class BookingBase(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
