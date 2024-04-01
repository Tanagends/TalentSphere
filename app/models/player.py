
from .basemodel import BaseModel
from sqlalchemy import Date 
from app import db


class Player(BaseModel):
    """Player model"""

    __tablename__ = 'players'

    surname = db.Column(db.String(120), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(120))
    club = db.Column(db.String(120), nullable=True)
    academy = db.Column(db.String(120), nullable=True)
    profile_image_path = db.Column(db.String(255))
    videos = db.relationship('Video', backref='player', lazy=True)
