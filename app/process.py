"""
  This function will be processing form base on the choose drop down list
"""
from flask import redirect, url_for


def process(field):
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
