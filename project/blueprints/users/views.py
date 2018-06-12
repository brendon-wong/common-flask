"""User blueprint."""
from flask import Blueprint, render_template, url_for, request, flash, redirect, abort, current_app
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from project.extensions import db, mail
from project.blueprints.users.decorators import anonymous_required, roles_required
from project.blueprints.users.forms import (UserForm, LoginForm, SettingsForm,
                                            UpdatePasswordForm, ResetPasswordForm)
from project.blueprints.users.models import User

users = Blueprint('users', __name__, template_folder='templates')


# Authentication


@users.route('/register', methods=["GET", "POST"])
@anonymous_required('/dashboard')
def register():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(full_name=form.data['full_name'],
                            preferred_name=form.data['preferred_name'],
                            email=form.data['email'],
                            password=form.data['password'])
            db.session.add(new_user)
            db.session.commit()
            # Log user in after registration
            login_user(new_user)
            # Confirm user email
            user_email = form.data['email']
            ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            user_confirmation_token = ts.dumps(user_email, salt="confirm-email")
            # Have Flask generate an external link
            confirm_url = url_for('users.confirm_email', token=user_confirmation_token, _external=True)
            html = render_template('users/mail/confirm_email.html', confirm_url=confirm_url, user=new_user)
            msg = Message("Please confirm your email", html=html, recipients=[user_email])
            mail.send(msg)
        except IntegrityError as e:
            flash("Email address already in use.")
            return render_template('users/register.html', form=form)
        flash('Successfully created account.')
        return redirect(url_for('main.dashboard'))
    return render_template('users/register.html', form=form)


@users.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        # Include max_age=86400 argument to have token expire in 1 day
        user_email = ts.loads(token, salt="confirm-email")
    except:
        # Abort if token is not valid
        abort(404)
    user = User.query.filter_by(email=user_email).first()
    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()
    # Log user in after email confirmed
    login_user(user)
    flash('Successfully logged in.')
    return redirect(url_for('main.dashboard'))


@users.route('/login', methods=["GET", "POST"])
@anonymous_required('/dashboard')
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(
                form.data['email'], form.data['password'])
            if user:
                # Modify this section if users do not have to confirm their email
                if user.email_confirmed:
                    login_user(user)
                    flash("Successfully logged in.")
                    return redirect(url_for('main.dashboard'))
                else:
                    flash("Please confirm your email before logging in.")
            else:
                flash("Incorrect email or password.")
    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('users.login'))


# User settings


@users.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm(obj=current_user)
    if request.method == "POST":
        if form.validate():
            if User.authenticate(current_user.email, form.data['password']):
                try:
                    current_user.full_name = form.data['full_name']
                    current_user.preferred_name = form.data['preferred_name']
                    current_user.email = form.data['email']
                    db.session.add(current_user)
                    db.session.commit()
                except IntegrityError as e:
                    flash("Email address already in use.")
                    return render_template('users/settings.html', form=form)
                flash('Successfully updated account.')
                return redirect(url_for('main.dashboard'))
            else:
                flash("Incorrect password.")
    return render_template('users/settings.html', form=form)


@users.route('/settings/update-password', methods=["GET", "POST"])
@login_required
def update_password():
    form = UpdatePasswordForm(request.form)
    if request.method == "POST":
        if form.validate():
            if User.authenticate(current_user.email, form.data['password']):
                current_user.password = User.encrypt_password(
                    form.data['new_password'])
                db.session.add(current_user)
                db.session.commit()
                flash('Successfully updated password.')
                return redirect(url_for('main.dashboard'))
            else:
                flash("Current password is incorrect.")
    return render_template('users/update_password.html', form=form)


@users.route('/reset-password', methods=["GET", "POST"])
@anonymous_required
def reset_password():

    # Edit; this is not proper functionality

    form = ResetPasswordForm(request.form)
    if request.method == "POST":
        if form.validate():
            if User.authenticate(current_user.email, form.data['password']):
                current_user.password = User.encrypt_password(
                    form.data['new_password'])
                db.session.add(current_user)
                db.session.commit()
                flash('Successfully updated password.')
                return redirect(url_for('main.dashboard'))
        flash("Current password is incorrect.")
    return render_template('users/reset_password.html', form=form)
