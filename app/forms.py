"""Module for declaring all form classes"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Email
from datetime import date
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
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
    password = PasswordField('Password', validators=[DataRequired(),
                             EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        """Check if email is already on the database"""
        users = [Sponsor, Club, Academy, Player, Scout]
        for User in users:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('please use a different email address')


class ScoutPlayerForm(BaseForm):
    """Player and scout base registration form"""

    surname = StringField('Surname', validators=[DataRequired(message="Please enter your surname"),
                                                 Length(min=2, max=36)])
    DOB = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender',  choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    club = StringField('Club', validators=[Length(max=36)])
    academy = StringField('Academy', validators=[Length(max=36)])
    profile_image_path = FileField("Profile Picture", validators=[FileAllowed(['jpg', 
                                   'jpeg', 'ico', 'tff', 'gif', 'png'], "Images only")])
    
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
    

class PlayerForm(ScoutPlayerForm):
    """Player registration form"""

    options = [("forward", "Forward"), ("midfielder", "Midfielder"),
               ("defender", "Defender"), ("goalkeeper", "Goalkeeper")]
    position = SelectField('Position', choices=options, validators=[DataRequired()])


class ScoutForm(ScoutPlayerForm):
    """Scout Registration Form"""
    def __init__(self, *args, **kwargs):
        super(ScoutForm, self).__init__(*args, **kwargs)
        self.academy.choices = [(None, 'None')] + [(a.id, a.name) for a in Academy.query.all()]
        self.club.choices = [(None, 'None')] + [(c.id, c.name) for c in Club.query.all()]

    club = SelectField('Club', validators=[Optional()])
    academy = SelectField('Academy', validators=[Optional()])

    def validate(self, extra_validators=None):

        if not super(ScoutForm, self).validate():
            return False

        if (self.academy.data == "None") and (self.club.data == "None"):
            self.academy.errors.append("Please select a club or an academy")
            self.club.errors.append("Please select a club or an academy")
            return False
        return True


class ClubForm(BaseForm):
    """Club registration form"""
    logo_path = FileField("Logo")#, validators=[FileAllowed(['jpg', 'png', 'jpeg',
                          #'ico', 'tff', 'gif'], "Images only")])


class AcademyForm(BaseForm):
    """Academy registration form"""
    logo_path = FileField("Logo")#, validators=[FileAllowed(['jpg', 'png',
                          #'jpeg', 'ico', 'tff', 'gif'], "Images only")])


class SponsorForm(BaseForm):
    """Sponsor registration form"""

    organization = StringField('Organization')
    gender = SelectField('Gender',  choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    profile_image_path = FileField("Profile Picture", validators=[FileAllowed(['jpg',
                                   'jpeg', 'ico', 'tff', 'gif','png'], "Images only")])


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('login')
