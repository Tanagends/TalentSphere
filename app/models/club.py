
from .basemodel import BaseModel
from app import db


class Club(BaseModel):
    """Club Model"""

    __tablename__ = 'clubs'

    scouts = db.relationship('Scout', backref='club', lazy=True)
    logo_path = db.Column(db.String(255))