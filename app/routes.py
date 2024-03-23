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
from app.process import process
from app import app
from app import db


@app.route('/')
@app.route('/index')
def index():
    """Landing page"""
    return f"Hello talentsphere"


@app.route('/signup/player', methods=['GET', 'POST'])
def player_form():
    """This function handle the logic for the player form"""
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    player = PlayerForm()
    if request.method == 'POST':
        role = request.form['role']
        process_result = process(role)
        
        if process_result:
            if player.validate_on_submit():
                players = {
                    'surname': player.surname.data,
                    'name': player.name.data,
                    'email': player.email.data,
                    'phone_number': player.phone_number.data,
                    'city': player.city.data,
                    'country': player.country.data,
                    'DOB': player.DOB.data,
                    'club': player.club.data,
                    'academy': player.academy.data,
                    'position': player.position.data,
                    'image_path': player.profile_image_path.data
                }
                player_user = Player(**players)
                player_user.set_password(player.password.data)
                db.session.add(player_user)
                db.session.commit()
                flash('Congratulations, you are now registered user!')
                return redirect(url_for('index'))
        else:
            flash('Invalid role selected.', 'error')
            redirect(url_for('index'))
    return render_template('signup.html', title='player signup', form=player)
