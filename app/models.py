from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, Date, Time, DateTime, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price_per_hour = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    work_start = Column(Time, nullable=False)
    work_end = Column(Time, nullable=False)
    bookings = relationship("Booking", back_populates="studio")
    reviews = relationship("Review", back_populates="studio")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    user = relationship("User", back_populates="bookings")
    studio = relationship("Studio", back_populates="bookings")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=False)

    user = relationship("User", back_populates="reviews")
    studio = relationship("Studio", back_populates="reviews")
