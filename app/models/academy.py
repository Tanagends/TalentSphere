
from .basemodel import BaseModel
from app import db


class Academy(BaseModel):
    """Academy Model"""

    __tablename__ = 'academies'

    scouts = db.relationship('Scout', backref='academy', lazy=True)
    logo_path = db.Column(db.String(255))