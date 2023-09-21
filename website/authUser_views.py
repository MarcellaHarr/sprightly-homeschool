# Import Packages & Extensions
from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import userAccount
from . import db

# Declare Blueprint object
authUser_views = Blueprint('authUser_views', __name__)

# Declare routes
@authUser_views.route("/")
def index():
    """Show Homepage"""
    return render_template('index.html', currentUser=current_user)

@authUser_views.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    register_flashes = {}
    if current_user.is_authenticated:
        return redirect(url_for('authUser_views.login'))
    if request.method == "POST":
        userFirstName = request.form['userFirstName']
        userLastName = request.form['userLastName']
        userEmail = request.form['userEmail']
        password = request.form['password']
        confirmation = request.form['confirmation']
        currentUser = userAccount.query.filter_by(userEmail = userEmail).first()
        if currentUser:
            register_flashes['dupAcct'] = "User already exists, please sign-in!"
        elif password != confirmation:
            register_flashes['missMatch'] = "Passwords don't match!"
        else:
            newUser = userAccount(userEmail = userEmail, 
                                  userFirstName = userFirstName, 
                                  userLastName = userLastName, 
                                  hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            register_flashes['succsAcct'] = "Account successfully created!"
            return redirect(url_for('dashUser_views.profile'))

    return render_template('register.html', register_flashes=register_flashes,
                           currentUser=current_user,
                           alert_types={'dupAcct': 'warning',
                                        'missMatch': 'dark',
                                        'succsAcct': 'success'})

@authUser_views.route("/login", methods=["GET", "POST"])
def login():
    """User log-in"""
    login_flashes = {}
    if current_user.is_authenticated:
        return redirect(url_for('dashUser_views.profile'))
    if request.method == "POST":
        userEmail = request.form.get('userEmail')
        password = request.form.get('password')
        session.clear()
        currentUser = userAccount.query.filter_by(userEmail = userEmail).first()
        if currentUser:
            if check_password_hash(currentUser.hash, password, method='pbkdf2:sha256'):
                login_user(currentUser, remember=True)
                login_flashes['logSuccessful'] = "Logged in successfully!"
                return redirect(url_for('dashUser_views.profile'))
            else:
                login_flashes['wrngPssw'] = "Incorrect password."
        else:
            login_flashes['wrngEmail'] = "Invalid email."

    return render_template('login.html', currentUser=current_user,
                           login_flashes=login_flashes,
                           alert_types={'logSuccessful': 'success',
                                          'wrngPssw': 'danger',
                                          'wrngEmail': 'dark'})


@authUser_views.route("/logout")
@login_required
def logout():
    """User sign-off"""
    loggdOut = "You have just logged out!"
    session.clear()
    session.pop('currentUser', None)
    logout_user()
    return redirect(url_for('authUser_views.login', loggdOut=loggdOut))


@authUser_views.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change user's password"""
    change_password_flashes = {}

    if request.method == "POST":
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')
        confirmation = request.form.get('confirmation')

        if not check_password_hash(current_user.hash, old_password, method='pbkdf2:sha256'):
            change_password_flashes['wrngOldPssw'] = "Incorrect old password."
        elif new_password != confirmation:
            change_password_flashes['missMatch'] = "Passwords don't match!"
        else:
            current_user.hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
            db.session.commit()
            change_password_flashes['succsPsswChange'] = "Password successfully changed!"

    return render_template('changePassword.html', currentUser=current_user,
                           change_password_flashes=change_password_flashes,
                           alert_types={'wrngOldPssw': 'danger',
                                        'missMatch': 'dark',
                                        'succsPsswChange': 'success'})


@authUser_views.route("/resetPasswordRequest", methods=["GET", "POST"])
def resetPasswordRequest():
    """Request to reset user's password"""
    reset_password_request_flashes = {}

    if current_user.is_authenticated:
        return redirect(url_for('authUser_views.index'))

    if request.method == "POST":
        userEmail = request.form.get('userEmail')
        new_password = request.form.get('newPassword')

        user = userAccount.query.filter_by(userEmail=userEmail).first()

        if user:
            """Update the user's password directly"""
            user.hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
            db.session.commit()

            reset_password_request_flashes['succsResetReq'] = "Password successfully reset."
        else:
            reset_password_request_flashes['userNotFound'] = "No user found with that email."

    return render_template('resetPasswordRequest.html', reset_password_request_flashes=reset_password_request_flashes,
                           alert_types={'succsResetReq': 'success',
                                        'userNotFound': 'danger'})
