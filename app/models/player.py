
from .basemodel import BaseModel
from sqlalchemy import Date 
from datetime import date
from app import db
import os


class Player(BaseModel):
    """Player model"""

    __tablename__ = 'players'

    surname = db.Column(db.String(120), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(120))
    position = db.Column(db.String(120))
    club = db.Column(db.String(120), nullable=True)
    academy = db.Column(db.String(120), nullable=True)
    profile_image_path = db.Column(db.String(255))
    videos = db.relationship('Video', backref='player', lazy=True)
    
    @property
    def age(self):
        """Calculate the actual age of a current user"""
        today = date.today()
        if self.DOB:
            age = today.year - self.DOB.year
            if ((today.month, today.day) < (self.DOB.month, self.DOB.day)):
                age -= 1
            return age
        else:
            return None
    
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
