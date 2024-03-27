from uuid import uuid4
from datetime import datetime, timezone
from app import db


class Video(db.Model):
    
    __tablename__ = "videos"
    
    id = db.Column(db.String(120), primary_key=True, default=uuid4())
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    video_path = db.Column(db.String(255))
    video_thumbnail_path = db.Column(db.String(255))
    player_id = db.Column(db.String(255), db.ForeignKey('players.id'))
