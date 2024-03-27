"""Module for declaring all form classes"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.player import Player
from app.models import Scout, Club, Academy, Sponsor
from app import db


class BaseForm(FlaskForm):
    """Base form inherited by all forms"""

    name = StringField('Name', validators=[DataRequired(message="Please enter your name"),
                       Length(min=2, max=36)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Mobile number', validators=[DataRequired(),
                               Length(min=5, max=15)])
    city = StringField('City', validators=[
                       DataRequired(), Length(min=2, max=36)])
    country = StringField('Country', validators=[
                          DataRequired(), Length(min=2, max=36)])
    postal_code = IntegerField('Postal code')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        """Check if email is already on the database"""
        users = [Sponsor, Club, Academy, Player, Scout]
        for User in users:
            user = User.query.filter_by(email=email).first()
        if user is not None:
            raise ValidationError('please use a different email address')


class ScoutPlayerForm(BaseForm):
    """Player and scout base registration form"""

    surname = StringField('Surname', validators=[DataRequired(message="Please enter your surname"),
                                                 Length(min=2, max=36)])
    DOB = DateField('Date of Birth', validators=[DataRequired()])
    club = StringField('Club', validators=[Length(min=2, max=36)])
    academy = StringField('Academy', validators=[Length(min=2, max=36)])
    profile_image_path = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'], "Images only")])
    
    def validate_name(self, surname):
        """Check if surname already on the database"""
        s_user = db.session.query(Scout).filter_by(Scout.surname == surname.data).all()
        
        if s_user is not None:
            raise ValidationError('Surname already exist, use different surname')
    

class PlayerForm(ScoutPlayerForm):
    """Player registration form"""

    position = StringField('Position', validators=[DataRequired(),
                           Length(min=2, max=36)])


class ScoutForm(ScoutPlayerForm):
    """Scout Registration Form"""
    pass


class ClubForm(BaseForm):
    """Club registration form"""
    logo_path = FileField("Logo", validators=[FileAllowed(['jpg', 'png'], "Images only")])


class AcademyForm(BaseForm):
    """Academy registration form"""
    logo_path = FileField("Logo", validators=[FileAllowed(['jpg', 'png'], "Images only")])


class SponsorForm(BaseForm):
    """Sponsor registration form"""

    organization = StringField('Organization')
    profile_image_path = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'], "Images only")])


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
