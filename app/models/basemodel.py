"""Talent Sphere BaseModel"""

from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import db

class BaseModel(db.Model):
    """Our Base Model to be inherited by all the other models"""

    __abstract__ = True

    id = db.Column(db.String(120), primary_key=True, default=uuid4())
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    email = db.Column(db.String(120), nullable=False)
    name =  db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    postal_code = db.Column(db.Integer)
    password = db.Column(db.String(2048))
    
    def set_password(self, passwd):
        """set a password for all other classes to inherit"""
        self.password = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        """check password to confirm before login in"""
        return check_password_hash(self.password, passwd)
