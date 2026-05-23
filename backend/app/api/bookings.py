from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.booking import Booking
from app.models.hotel import Room
from app.schemas.booking import BookingCreate, BookingResponse
from app.auth.dependencies import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    if not room.is_available:
        raise HTTPException(status_code=400, detail="Room is not available")
        
    # Simple total price calculation based on nights (assuming 1 night for simplicity here, can be extended)
    delta = booking.check_out_date - booking.check_in_date
    nights = delta.days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Invalid dates")
        
    total_price = nights * room.price_per_night

    new_booking = Booking(
        user_id=current_user.id,
        room_id=room.id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_price=total_price,
        status="confirmed"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=List[BookingResponse])
def get_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    booking.status = "cancelled"
    db.commit()
    return None
