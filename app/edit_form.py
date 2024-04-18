"""Module to handle all user profile"""

from flask_wtf import FlaskForm
from datetime import date
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email


class EditBaseForm(FlaskForm):
    """Base form for all users"""
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=200)])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = IntegerField('Postal Code')
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    profile_image_path = FileField('Profile Picture', validators=[
                            FileAllowed(['jpg', 'png', 'jpeg'], "Images only")])
    submit = SubmitField('Save Changes')


class PlayerScoutEditForm(EditBaseForm):
    """Base form for player and scout"""
    club = StringField('Club', validators=[Length(max=36)])
    academy = StringField('Academy', validators=[Length(max=36)])
    DOB = DateField('Date Of Birth', validators=[DataRequired()])

class PlayerEditForm(PlayerScoutEditForm, EditBaseForm):
    """Player edit form"""
    pass

class ScoutEditForm(PlayerScoutEditForm, EditBaseForm):
    """Scout edit form"""
    pass

class SponsorEditForm(EditBaseForm):
    """Sponsor edit form"""
    organization = StringField('Organization')


class ClubAcademyEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    logo_path = FileField("Logo", validators=[
                          FileAllowed(['jpg', 'png', 'jpeg'], "Images only")])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=200)])
    submit = SubmitField('Submit')


class ClubEditForm(ClubAcademyEditForm):
    """Club registration form"""
    pass


class AcademyEditForm(ClubAcademyEditForm):
    """Academy registration form"""
    pass
