"""Our views for the Talent Sphere Application"""
from flask import render_template, redirect, url_for, flash, Blueprint, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from flask import request, session
from sqlalchemy.exc import SQLAlchemyError
from app.edit_form import EditBaseForm, ClubAcademyEditForm, PlayerScoutEditForm
from app.edit_form import PlayerEditForm, ScoutEditForm, SponsorEditForm
from app.edit_form import ClubEditForm, AcademyEditForm
from app.models.basemodel import BaseModel
from app.models.player import Player
from app.models.scout import Scout
from app.models.club import Club
from app.models.academy import Academy
from app.models.sponsor import Sponsor
from config import Config
from sqlalchemy import func
from datetime import datetime
import os
from functools import reduce
from app import db


main_app = Blueprint('main2', __name__)


@main_app.route('/home')
#@login_required
def home():
    """Home page"""
    user_type = session.get('user_type')
    return render_template('home.html', user_type=user_type)


@main_app.route('/players', methods=['GET'])
def filter_players():
    """Route to filter player base on age, gender, and position"""
    age = request.form.get('age')
    gender = request.form.get('gender')
    position = request.form.get('position')

    filtered_players = player_filter(age, gender, position)
    return render_template('home.html', filtered_players=filtered_players)


def player_filter(age, gender, position):
    """Filter players"""

    queries = db.session.query(Player)

    # Age filtering
    if age is not None:
        age_query = queries.filter(func.DATEDIFF(
            func.current_date(), Player.DOB) / 365 == age)
    else:
        age_query = None

    # Gender filtering
    if gender is not None:
        gender_query = queries.filter(Player.gender == gender)
    else:
        gender_query = None

    # Position filtering
    if position is not None:
        player_query = queries.filter(Player.position == position)
    else:
        player_query = None

    # combine filtering
    filtered_queries = [age_query, gender_query, player_query]

    if any(q is None for q in filtered_queries):
        filtered_player = db.session.query(Player).all()
    else:
        filtered_player = reduce(set.intersection, [set(
            query.all()) for query in filtered_queries])
    return list(filtered_player)


@main_app.route('/profile', methods=['GET', 'POST'], endpoint='profile')
def profile():
    """Route to edit user profile"""
    
    user_type = session.get('user_type')
    profile_helper = handle_profile(user_type)
    return profile_helper


def handle_profile(user_type):
    """This function is meant to achieve switch case in python
    to handle user edit profiles base on the user_type
    
    list of user_type = [players, scouts, sponsors, club, academies]
    """
    
    user_type_mapping = {
        'player': (PlayerEditForm, 'player_profile.html'),
        'scout': (ScoutEditForm, 'scout_profile.html'),
        'sponsor': (SponsorEditForm, 'sponsor_profile.html'),
        'club': (ClubEditForm, 'club_profile.html'),
        'academy': (AcademyEditForm, 'academy_profile.html')
    }
    
    #Get form class and template name based on user_type
    form_class, template_name = user_type_mapping.get(user_type, (None, None))
    
    #check if form_class and template_name is not None
    if form_class is None or template_name is None:
        flash("Unsupported user type", 'error')
        return redirect(url_for('main2.profile', user_type=user_type))
    
    form = form_class()
    if form.validate_on_submit():
        #process form data based on user_type
        if user_type in ['player', 'scout']:
            process_player_scout_form(form)
        elif user_type == 'sponsor':
            process_sponsor_form(form)
        elif user_type in ['club', 'academy']:
            process_club_academy_form(form)
        
       #commit changes to the database
        try:
           db.session.commit()
           flash("Congratulation, changes saved successfully", 'success')
           return redirect(url_for('main2.profile', user_type=user_type))
        except SQLAlchemyError:
           db.session.rollback()
           flash("An error occurred while updating your profile", 'error')
           return redirect(url_for('main2.profile', user_type=user_type))
    elif request.method == 'GET':
        #Populate form field with current user data
        populate_form_field(form, user_type)
    return render_template(template_name, form=form, user_type=user_type)  
        

def process_player_scout_form(form):
    """Process player and scout form"""
    current_user.name = form.name.data
    current_user.bio = form.bio.data
    current_user.DOB = form.DOB.data
    current_user.gender = form.gender.data
    current_user.country = form.country.data
    current_user.city = form.city.data
    current_user.postal_code = form.postal_code.data
    current_user.club = form.club.data
    current_user.academy = form.academy.data
    current_user.email = form.email.data
    
    file = form.profile_image_path.data
    file_path = upload_file(file)
        
    #check if not None
    if file and file_path:
        current_user.save(file, file_path) #save the file


def process_sponsor_form(form):
    """Proccess sponsor form"""
    current_user.name = form.name.data
    current_user.bio = form.bio.data
    current_user.gender = form.gender.data
    current_user.country = form.country.data
    current_user.city = form.city.data
    current_user.postal_code = form.postal_code.data
    current_user.email = form.email.data
    current_user.organization = form.organization.data
    
    file = form.profile_image_path.data
    file_path = upload_file(file)
        
    #check if not None
    if file and file_path:
        current_user.save(file, file_path) #save the file
    

def process_club_academy_form(form):
    current_user.name = form.name.data
    current_user.bio = form.bio.data
    
    file = form.logo_path.data
    file_path = upload_file(file)
    
    #check if not None
    if file and file_path:
        current_user.save(file, file_path)
        

def populate_form_field(form, user_type):
    """Populate form fields with current user data based on user type."""
    
    #common fields
    form.name.data = current_user.name
    form.bio.data = current_user.bio
    
    if user_type in ['player', 'scout']:
        form.DOB.data = current_user.DOB
        form.gender.data = current_user.gender
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.club.data = current_user.club
        form.academy.data = current_user.academy
        form.email.data = current_user.email
        form.profile_image_path.data = current_user.profile_image_path

    elif user_type == 'sponsor':
        form.gender.data = current_user.gender
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.email.data = current_user.email
        form.profile_image_path.data = current_user.profile_image_path
        form.organization.data = current_user.organization

    elif user_type in ['club', 'academy']:
        form.logo_path.data = current_user.logo_path


def upload_file(file_to_upload):
    """Function to upload a file to the specified path
    - file_to_upload: file to upload
    """
    uploaded_files = file_to_upload
    
    if not file_to_upload:
        return None
    

    filename = secure_filename(uploaded_files.filename)
    uploaded_dir = current_app.config['UPLOAD_IMAGES']
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), uploaded_dir, filename)
    
    try:
        file_to_upload.save(file_path)  # Save the file to the specified path
        return file_path
    except Exception as e:
        # Handle file save errors
        print(f"Error saving file: {e}")
        return None
