"""Module for declaring all form classes"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class BaseForm(FlaskForm):
    """Base form inherited by all forms"""

    name = StringField('Name', validators=
                       [DataRequired(message="Please enter your name"),
                       Length(min=2, max=36))
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Mobile number', validators=[DataRequired(),
                               Length(min=5, max=15)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=36)])
    country = StringField('Postal code', validators=[DataRequired(), Length(min=2, max=36])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators[DataRequired(),
                                     EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class ScoutPlayerForm(BaseForm):
    """Player and scout base registration form"""

    surname = StringField('Surname', validators=
                       [DataRequired(message="Please enter your surname"),
                       Length(min=2, max=36))
    DOB = StringField('Date of Birth', validators=[DataRequired()])
    club = StringField('Club', validators=[Length(min=2, max=36)])
    academy = StringField('Academy', validators=[Length(min=2, max=36)])


class PlayerForm(ScoutPlayerForm):
    """Player registration form"""

    position = StringField('Position', validators=[Datarequired(),
                           Length(min=2, max=36)])
    


class ScoutForm(ScoutPlayerForm):
    """Scout Registration Form"""
    pass


class ClubForm(BaseForm):
    """Club registration form"""
    pass


class AcademyForm(BaseForm):
    """Academy registration form"""
    pass


class SponsorForm(BaseForm):
    """Sponsor registration form"""

    organization = StringField('Organization')
