
from .basemodel import BaseModel
from sqlalchemy import Date 
from app import db
import os


class Scout(BaseModel):
    """Scout Model"""

    __tablename__ = 'scouts'
    """
    __table_args__ = (
                    db.CheckConstraint(text("(club_id IS NOT NULL) OR (academy_id IS NOT NULL)"), name='chk_scout_affiliation'),
                        )
    """

    surname = db.Column(db.String(120), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(120))
    profile_image_path = db.Column(db.String(255))
    club_id = db.Column(db.String(120), db.ForeignKey('clubs.id'), nullable=True)
    academy_id = db.Column(db.String(120), db.ForeignKey('academies.id'), nullable=True)
    
    def save(self, uploaded_file, file_path):
        """method to save the uploaded file to the specified file path.
         
          - file_path: the path to save the file
        """
        
        if file_path:
            with open(file_path, 'wb') as file:
                file.write(uploaded_file.read())
            
            #calculate the path relative to the static directory
            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            relative_path = os.path.relpath(file_path, static_dir)
            self.profile_image_path = relative_path
