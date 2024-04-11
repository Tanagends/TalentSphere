"""Talent Sphere BaseModel"""

from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import db

class BaseModel(db.Model):
    """Our Base Model to be inherited by all the other models"""

    __abstract__ = True

    id = db.Column(db.String(120), primary_key=True, default= lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    email = db.Column(db.String(120), nullable=False)
    name =  db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    postal_code = db.Column(db.Integer)
    bio = db.Column(db.String(250))
    password = db.Column(db.String(2048), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)
    # role = ""

    def is_active(self):
        """Check if the user account is active"""
        return self.is_active
    
    def get_id(self):
        """Return the unique identifier for the user"""
        return self.id

    def is_authenticated(self):
        """Check if the user is authenticated"""
        return True  # Assuming all users are authenticated

    # def is_active(self):
    #     """Check if the user account is active"""
    #     return True  # Assuming all user accounts are active

    def is_anonymous(self):
        """Check if the user is anonymous"""
        return False  # Assuming no anonymous users
    
    def set_password(self, passwd):
        """set a password for all other classes to inherit"""
        self.password = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        """check password to confirm before login in"""
        return check_password_hash(self.password, passwd)



#Create a role in the database to determine user base on role
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Role {self.name}>'