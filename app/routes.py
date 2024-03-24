"""Our views for the Talent Sphere Application"""
from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from flask import request
from app.forms import BaseForm
from app.forms import ScoutPlayerForm
from app.forms import PlayerForm
from app.forms import ScoutForm
from app.forms import ClubForm
from app.forms import AcademyForm
from app.forms import SponsorForm
from app.models.player import Player
from app.models.scout import Scout
from app.models.club import Club
from app.models.academy import Academy
from app.models.sponsor import Sponsor
from app.process import base_fields, user_signup_helper
from app import app
from app import db


@app.route('/')
@app.route('/index')
def index():
    """Landing page"""

    return f"Hello talentsphere"


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """The signup page to get the user role"""

    if request.method == "GET":
        return render_template("signup.html")
    
    field = request.form['role']

    if field == 'Football player':
        return redirect(url_for('player_signup'))
    elif field == 'Scout':
        return redirect(url_for('scout_signup'))
    elif field == 'Football club':
        return redirect(url_for('club_signup'))
    elif field == 'Football Academy':
        return redirect(url_for('football_signup'))
    elif field == 'Sponsor':
        return redirect(url_for('sponsor_signup'))
    else:
        flash("Invalid option")    


@app.route('/signup/player', methods=['GET', 'POST'])
def player_signup():
    """Handles the logic for the player signup"""
 
    return user_signup_helper(PlayerForm, Player, 'player_signup.html', 'Football Player')


@app.route('/signup/scout', methods=['GET', 'POST'])
def scout_signup():
    """Handles the logic for the scout signup"""
 
    return user_signup_helper(ScoutForm, Scout, 'scout_signup.html', 'Football Scout')


@app.route('/signup/club', methods=['GET', 'POST'])
def club_signup():
    """Handles the logic for the club signup"""
 
    return user_signup_helper(ClubForm, Club, 'club_signup.html', 'Football Club')


@app.route('/signup/academy', methods=['GET', 'POST'])
def academy_signup():
    """Handles the logic for the academy signup"""
 
    return user_signup_helper(AcademyForm, Academy, 'academy_signup.html', 'Football Academy')


@app.route('/signup/sponsor', methods=['GET', 'POST'])
def sponsor_form():
    """Handles the logic for the sponsor signup"""
 
    return user_signup_helper(SponsorForm, Sponsor, 'sponsor_signup.html', 'Football Sponsor')


@app.route('/login')
def login():
    """Logs in the user"""
