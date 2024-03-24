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
from app.process import base_fields
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
        return redirect(url_for('/signup/player'))
    elif field == 'Scout':
        return redirect(url_for('scout_form'))
    elif field == 'Football club':
        return redirect(url_for('club_form'))
    elif field == 'Football Academy':
        return redirect(url_for('football_form'))
    elif field == 'Sponsor':
        return redirect(url_for('sponsor_form'))
    else:
        flash("Invalid option")
    



@app.route('/signup/player', methods=['GET', 'POST'])
def player_form():
    """This function handle the logic for the player form"""
 
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = PlayerForm()
    if form.validate_on_submit():
        player_dict = base_fields(form)
        player_user = Player(**player_dict)
        player_user.set_password(player.password.data)
        db.session.add(player_user)
        db.session.commit()
        flash('Congratulations, you are now registered user!')
        return redirect(url_for('index'))

    return render_template('signup.html', title='player signup', form=player)
