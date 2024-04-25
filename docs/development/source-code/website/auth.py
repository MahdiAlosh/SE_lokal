from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) # POST: for sending informations to server, GET: URL request in URL-bar
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #print(password)
        user = User.query.filter_by(email=email).first() # looking for speciffic Column: filter all the users, that have this email
        #print(f'Eingegebenes Passwort: {password}')
     
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # save the section
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    #data = request.form
    #print(data)
    return render_template("login.html", user=current_user) # variable uebergeben
    #(, text="Testing") how to pass values to tamlpates 

@auth.route('/logout')
@login_required # um sicher zu stellen, dass man erst logged in, dann darf logout 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


""" 
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if  request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) # save the section
            flash('Account created!', category='success')
            
            print(password1)
            print(password2)
            
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user) 
"""



'''
### fuer Loeschen eines vorhandenen users!

    email_to_delete = 'ali@gmail.com'
    user_to_delete = User.query.filter_by(email=email_to_delete).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        print(f'Benutzer mit E-Mail {user_to_delete.email} wurde gelöscht.')
    else:
        print('Benutzer nicht gefunden.')
'''