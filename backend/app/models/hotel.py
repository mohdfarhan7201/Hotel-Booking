from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    city = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    stars = Column(Integer, default=1)
    rating = Column(Float, default=0.0)
    amenities = Column(JSON, nullable=True) # List of amenities
    images = Column(JSON, nullable=True) # List of image URLs
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    type = Column(String, nullable=False) # e.g., Deluxe, Suite
    description = Column(Text, nullable=True)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    amenities = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)
    is_available = Column(Boolean, default=True)

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")
