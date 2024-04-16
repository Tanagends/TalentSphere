
from .basemodel import BaseModel
from app import db
import os


class Club(BaseModel):
    """Club Model"""

    __tablename__ = 'clubs'

    scouts = db.relationship('Scout', backref='club', lazy=True)
    logo_path = db.Column(db.String(255))
    
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
            self.logo_path = relative_path
