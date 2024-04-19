"""
  This module has all our helper functions for the views / routes
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from uuid import uuid4
import os
from werkzeug.utils import secure_filename
from app import db


def upload_profile_image(profile):
    """Uploads the profile picture and returns the name"""
    if not profile:
        return
    filen, ext = os.path.splitext(profile.filename)
    filenam = os.path.join(str(uuid4()) + ext)
    filename = secure_filename(filenam)
    profile.filename = filename
    filepath = os.path.join('/static/profile_pics/', filename)
    try:
        profile.save(filepath)
    except Exception as e:
        print("Error saving file:", e)
    return filepath


def base_fields(form):
    """Returns a dict of a base form of fields common to all users"""

    common_fields_dict = {
        'name': form.name.data,
        'email': form.email.data,
        'phone_number': form.phone_number.data,
        'city': form.city.data,
        'country': form.country.data,
        'postal_code': form.postal_code.data
    }

    #Checking if they are a player or scout to add the common fields
    if form.data.get('surname'):
        distinct_fields = {
                'surname': form.surname.data,
                'DOB': form.DOB.data,
                'gender': form.gender.data,
                'profile_image_path': upload_profile_image(form.profile_image_path.data)
        }

        # Adding the position, club, academy fields if it's a player
        if form.data.get('position') and distinct_fields:
            distinct_fields['position'] = form.position.data
            distinct_fields['club'] = form.club.data
            distinct_fields['academy'] = form.academy.data

        #Else adding club or academy id's for a scout
        else:
            distinct_fields['club_id'] = form.club.data if form.club.data != "None" else None
            distinct_fields['academy_id'] = form.academy.data if form.academy.data != "None" else None

    #Checking if they are an organization to add organization and image fields
    elif form.data.get('organization'):

        distinct_fields = {
                'organization': form.organization.data,
                'profile_image_path': upload_profile_image(form.profile_image_path.data)
        }
    
    #Checking if they are a club or academy, and setting their unique field
    else:
        distinct_fields = {
                'logo_path': upload_profile_image(form.logo_path.data)
        }

    common_fields_dict.update(distinct_fields)
    return common_fields_dict


def user_signup_helper(Form, User, htm, usr):
    """Generic user creation and database save function"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = Form()

    if form.validate_on_submit():
        user_dict = base_fields(form)
        print(user_dict)
        user = User(**user_dict)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered user!')
        return redirect(url_for('main.login'))

    return render_template(htm, user=usr, form=form)
