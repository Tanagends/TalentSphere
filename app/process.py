"""
  This module has all our helper functions for the views / routes
"""
from flask import redirect, url_for
from uuid import uuid4
import os
from werkzeug.utils import secure_filename

def upload_profile_image(profile):
    """Uploads the profile picture and returns the name"""
    filen, ext = os.path.splitext(profile.filename)
    filenam = os.path.join(str(uuid4()), ext)
    filename = secure_filename(filenam)
    filepath = os.path.join('static/profile_pics/', filename)
    profile.save(filepath)
    return filepath

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

def base_fields(form):
    """Returns a dict of a base form of fields common to all users"""

    common_fields_dict = {
        'name': form.name.data,
        'email': form.email.data,
        'phone_number': form.phone_number.data,
        'city': form.city.data,
        'country': form.country.data,
    }

    #Checking if they are a player or scout to add the common fields
    if form.data.get('surname'):
        distinct_fields = {
                'surname': form.surname.data,
                'DOB': form.DOB.data,
                'club': form.club.data,
                'academy': form.academy.data,
                'profile_image_path': upload_profile_image(form.profile_image_path.data)
        }

        # Adding the position field if it's a player
        if form.data.get('position') and distinct_fields:
            distinct_fields['position'] = form.position.data

    #Checking if they are an organization to add an organization and image field 
    elif form.data.get('organization'):

        distinct_fields = {
                'organization': form.organization.data,
                'profile_image_path': upload_profile_image(form.profile_image_path.data)
        }
    
    #They are a club or academy, and this sets their unique fields
    else:
        distinct_fields = {
                'logo_path' = upload_profile_image(form.profile_image_path.data)
        }

    return common_fields_dict.update(distinct_fields)
