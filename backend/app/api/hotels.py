from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelResponse
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/hotels", tags=["hotels"])

@router.get("/", response_model=List[HotelResponse])
def get_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hotels = db.query(Hotel).offset(skip).limit(limit).all()
    return hotels

@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@router.post("/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    new_hotel = Hotel(**hotel.model_dump())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
        
    db.delete(hotel)
    db.commit()
    return None
