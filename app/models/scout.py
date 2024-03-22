
from .basemodel import BaseModel
from sqlalchemy import Date 
from app import db


class Scout(BaseModel):
    """Scout Model"""

    __tablename__ = 'scouts'
    """
    __table_args__ = (
                    db.CheckConstraint(text("(club_id IS NOT NULL) OR (academy_id IS NOT NULL)"), name='chk_scout_affiliation'),
                        )
    """

    surname = db.Column(db.String(120), nullable=False)
    DOB = db.Column(Date, nullable=False)
    profile_image_path = db.Column(db.String(255))
    club_id = db.Column(db.String(120), db.ForeignKey('clubs.id'), nullable=True)
    academy_id = db.Column(db.String(120), db.ForeignKey('academies.id'), nullable=True)