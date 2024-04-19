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
from sqlalchemy import func
from app import db
from app import login_manager
from app.routes import main_app
from sqlalchemy import and_, or_
from datetime import datetime
from sqlalchemy import or_, and_

main3 = Blueprint('main3', __name__)
"""
@main3.route('/profile')
def profile():
    return render_template('profile.html')
"""

@main3.route('/profile/<string:id>', strict_slashes=False)
def profile(id):
    
    player = Player.query.get(id)
    """
    pl_dict = {k: v for k, v in player.__dict__.items() if k in Player.__table__.columns.keys()}
    pl_dict.pop('email', None)
    pl_dict.pop('password', None
    """
    return render_template('profile.html', player=player)


@main3.route('/profiles', methods=["GET", "POST"], strict_slashes=False)
def profiles():


    #excluded_fields = ["password", "email"]

    if request.method == "GET":
        players = Player.query.order_by(db.func.random()).limit(12).all()
        """
        dict_list = []
        for player in players:
            dict_list.append({k: v for k, v in player.__dict__.items()
                             if k in Player.__table__.columns.keys() and not k in excluded_fields})
        """
        return render_template('profiles.html', players=players)

    else:
        query = db.session.query(Player)
        
        if request.form.get('gender'):
            gender = request.form.get('gender')
            query = query.filter_by(gender=gender)

        if request.form.get('position'):
            position = request.form.get('position')
            query = query.filter_by(position=position)

        if request.form.get('search'):
            search = request.form.get('search')
            query = query.filter(or_(Player.name.contains(search), Player.surname.contains(search)))

        age = request.form.get('age')

        if age == "U15":
            min_age, max_age = 0, 15
        elif age == "U18":
            min_age, max_age = 15, 18
        elif age == "U21":
            min_age, max_age = 18, 21
        elif age == "U23":
            min_age, max_age = 18, 23
        elif age == "Above 23":
            min_age, max_age = 23, 500
        else:
            min_age, max_age = None, None

        if min_age and max_age:
            plyrs = query.all()
            players = []
            for player in plyrs:
                if len(players) < 12 and min_age <= player.age < max_age:
                    players.append(player)
            #query = query.filter(and_(age_expr >= min_age, age_expr < max_age))
        else:    
            players = query.limit(12).all()

        return render_template('profiles.html', players=players)

    """
    search_dict = {}
    search_lis = [k == v for k, v in search_dict.items()]

    age = "U23"#request.form.get('age')

    if age == "U15":
        min_age, max_age = 0, 15
    elif age == "U18":
        min_age, max_age = 15, 18
    elif age == "U23":
        min_age, max_age = 18, 23
    elif age == "Above 23":
        min_age, max_age = 23, 50
    else:
        min_age, max_age = 3, 50

    age_expr = (db.extract('year', db.func.now()) - db.extract('year', Player.DOB)) -\
                ((db.extract('month', db.func.now), db.extract('day', db.func.now())) < (db.extract('month', Player.DOB), db.extract('day', Player.DOB)))
    
    if not (min_age == 3 and max_age == 50):
        print("valid search range")
        search_list = search_lis + [age_expr >= min_age, age_expr < max_age]
    else:
        search_list = search_lis

    search_str = '%' + '' + '%' #request.form.get('search') + '%'
    search_fields = [Player.name.ilike(search_str), Player.surname.ilike(search_str)]
    
    if search_str != '%%':
        players = Player.query.filter(and_(*search_list, or_(*search_fields))).limit(10).all()
    else:
        print("no search field used")
        players = Player.query.filter(and_(*search_list)).limit(10).all()

    print("Number of search results:", len(players))
    player = players[0]

    print(f"Name and Surname: {player.name} {player.surname}\nDOB: {player.DOB}")

    return render_template('profiles.html')
    """
