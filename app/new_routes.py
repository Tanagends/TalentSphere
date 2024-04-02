"""MY application"""
from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from app.forms import BaseForm
from app.forms import ScoutPlayerForm
from app.forms import PlayerForm
from app.forms import ScoutForm
from app.forms import ClubForm
from app.forms import AcademyForm
from app.forms import SponsorForm, LoginForm
from app.models.basemodel import BaseModel
from app.models.player import Player
from app.models.scout import Scout
from app.models.club import Club
from app.models.academy import Academy
from app.models.sponsor import Sponsor
from app.process import base_fields, user_signup_helper
from app import db
from app import login_manager
from app.routes import main_app

@main_app.route('/profile/<str:id>', strict_slashes=False)
def profile(id):
    """Displays the profile of the player"""

    player = Player.query.get(id)
    pl_dict = {k: v for k, v in player.__dict__.items() if k in Player.__columns__}
    pl_dict.pop('email', None)
    pl_dict.pop('password', None)

    return render_template('profile.html', player=pl_dict)

@main_app.route('profiles', methods=["GET", "POST"], strict_slashes=False)
def profiles():
    """Shows the profiles of the players"""
    excluded_fields = ["password", "email"]

    if request.method == "GET":
        players = Player.query.order_by(db.func.random()).limit(10).all()
        dict_list = []
        for player in players:
            dict_list.append({k: v for k, v in player.__dict__.items()
                             if k in Player.__columns__ and not k in excluded_fields})
        return render_template('profiles.html', profiles=dict_list)

    else:
        search_dict = {}
        if request.form.get('gender'):
            search_dict['gender'] = request.form.get('gender')
        if request.form.get('position'):
            search_dict['position'] = request.form.get('position')
        if request.form.get('age'):

            search_dict['age'] = request.form.get('age')

        search_str = request.form.get('search')
        
        players = Player.query.filter_by(**search_dict)
