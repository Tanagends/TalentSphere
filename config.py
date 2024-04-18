"""Talent Sphere configuration settings file"""

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = "mysql://talent_admin:talent_pwd@localhost/talent_sphere"
    
    UPLOAD_IMAGES = 'static/images'
    UPLOAD_VIDEOS = 'static/videos'