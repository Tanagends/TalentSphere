
from .basemodel import BaseModel
from app import db


class Sponsor(BaseModel):
    """Sponsor Model"""

    __tablename__ = 'sponsors'

    organization = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(120))
    profile_image_path = db.Column(db.String(255))