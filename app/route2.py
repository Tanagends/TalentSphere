"""Our views for the Talent Sphere Application"""
from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from app.edit_form import EditBaseForm, ClubAcademyEditForm
from app.edit_form import PlayerEditForm, ScoutEditForm, SponsorEditForm
from app.edit_form import ClubEditForm, AcademyEditForm
from app.models.basemodel import BaseModel
from app.models.player import Player
from app.models.scout import Scout
from app.models.club import Club
from app.models.academy import Academy
from app.models.sponsor import Sponsor
from sqlalchemy import func
from datetime import datetime
from functools import reduce
from app import db


main_app = Blueprint('main2', __name__)


@main_app.route('/home')
@login_required
def home():
    """Home page"""
    return render_template('index.html')


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


@main_app.route('/edit_profile/<user_type>', methods=['GET', 'POST'])
def profile(user_type):
    """Route to edit user profile"""
    form, template = get_edit_form_usertype(user_type)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.dob = form.DOB.data
        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        current_user.club = form.club.data
        current_user.academy = form.academy.data
        current_user.organization = form.organization.data
        try:
            db.session.commit()
            flash("Congratulation, changes saved successfully", 'success')
            return redirect(f'/edit_profile/{user_type}')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Oops! there was an error in your update", 'error')
            return redirect(f"/edit_profile/{user_type}")
    elif request.method == 'GET':

        form.name.data = current_user.name
        form.bio.data = current_user.bio
        form.DOB.data = current_user.DOB
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.club.data = current_user.club
        form.academy.data = current_user.academy
        form.organization.data = current_user.organization
    return render_template(template, form=form, user_type=user_type)


# academy and club view function
@main_app.route('/edit_club/<user_type>', methods=['GET', 'POST'])
def edit_club(user_type):
    """Route to edit club"""
    club_academy_form, template = get_edit_form_usertype(user_type)

    if club_academy_form.validate_on_submit():
        current_user.logo_path = club_academy_form.logo_path.data
        current_user.bio = club_academy_form.bio.data
        try:
            db.session.commit()
            flash("Congratulation, changes saved successfully", 'success')
            return redirect("/edit_club/{user_type}")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Oops! there was an error in your update", 'error')
            return redirect('/edit_club/{user_type}')
    elif request.method == 'GET':
        club_academy_form.logo_path.data = current_user.logo_path
        club_academy_form.bio.data = current_user.bio
    return render_template(template, form=club_academy_form)

# user_type function
def get_edit_form_usertype(user_type):
    """Function to get user edit form"""

    if user_type == 'players':
        return PlayerEditForm(), 'player_profile.html'
    elif user_type == 'scouts':
        return ScoutEditForm(), 'scout_profile.html'
    elif user_type == 'sponsors':
        return SponsorEditForm(), 'sponsor_profile.html'
    elif user_type == 'clubs':
        return ClubEditForm(), 'club_profile.html'
    elif user_type == 'academies':
        return AcademyEditForm(), 'academy_profile.html'
    else:
        return None, None

# Get user id
# def get_user_id(user_type, user_id):
#     """Function to get user id"""
# 
#     if user_type == 'player':
#         user = Player.query.get(user_id)
#     elif user_type == 'scout':
#         user = Scout.query.get(user_id)
#     elif user_type == 'sponsor':
#         user = Sponsor.query.get(user_id)
#     else:
#         user = None
# 
#     return user
# 
