"""Module to handle all user profile"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class EditBaseForm(FlaskForm):
    """Base form for all users"""
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=200)])
    DOB = DateField('Date Of Birth', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = IntegerField('Postal Code')
    profile_pic = FileField('Profile Picture', validators=[
                            FileAllowed(['jpg', 'png'], "Images only")])
    submit = SubmitField('Save Changes')


class PlayerEditForm(EditBaseForm):
    """Player edit form"""
    club = StringField('Club', validators=[Length(max=36)])
    academy = StringField('Academy', validators=[Length(max=36)])


class ScoutEditForm(EditBaseForm):
    """Scout edit form"""
    club = StringField('Club', validators=[Length(max=36)])
    academy = StringField('Academy', validators=[Length(max=36)])


class SponsorEditForm(EditBaseForm):
    """Sponsor edit form"""
    organization = StringField('Organization')


class ClubAcademyEditForm(FlaskForm):
    logo_path = FileField("Logo", validators=[
                          FileAllowed(['jpg', 'png'], "Images only")])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=200)])
    submit = SubmitField('Submit')


class ClubEditForm(ClubAcademyEditForm):
    """Club registration form"""
    pass


class AcademyEditForm(ClubAcademyEditForm):
    """Academy registration form"""
    pass
