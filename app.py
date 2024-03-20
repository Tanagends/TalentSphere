"""TalentSphere Application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ""
db = SQLAlchemy(app)

class BaseModel(db.Model):
    """Our Base Model to be inherited by all the other models"""

    __abstract__ = True

    id = db.Column(db.String, primary_key=True, default=uuid4())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email = db.Column(db.String, nullable=False)
    name =  db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    city = db.Column(db.String)
    country = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    password = db.Column(db.String)


class Player(BaseModel):
    """Player model"""

    __tablename__ = 'players'

    surname = db.Column(db.String, nullable=False)
    DOB = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String)
    club = db.Column(db.String)
    academy = db.Column(db.String)


class Scout(BaseModel):
    """Scout Model"""

    __tablename__ = 'scouts'
    """
    __table_args__ = (
                    db.CheckConstraint(text("(club_id IS NOT NULL) OR (academy_id IS NOT NULL)"), name='chk_scout_affiliation'),
                        )
    """

    surname = db.Column(db.String, nullable=False)
    DOB = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.String, db.ForeignKey('clubs.id'), nullable=True)
    academy_id = db.Column(db.String, db.ForeignKey('academies.id'), nullable=True)


class Club(BaseModel):
    """Club Model"""

    __tablename__ = 'clubs'

    scouts = db.relationship('Scout', backref='club', lazy=True)

class Academy(BaseModel):
    """Academy Model"""

    __tablename__ = 'academies'

    scouts = db.relationship('Scout', backref='academy', lazy=True)


class Sponsor(BaseModel):
    """Sponsor Model"""

    __tablename__ = 'sponsors'

    organization = db.Column(db.String, nullable=True)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
