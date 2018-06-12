"""User blueprint."""
from flask import Blueprint, render_template, url_for, request, flash, redirect, abort, current_app
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from project.extensions import db
from project.utils.email import send_email
from project.blueprints.users.decorators import anonymous_required, roles_required
from project.blueprints.users.forms import (UserForm, LoginForm, SendConfirmEmailForm,
                                            SettingsForm, UpdatePasswordForm,
                                            SendResetEmailForm, ResetPasswordForm)
from project.blueprints.users.models import User

users = Blueprint('users', __name__, template_folder='templates')


# Login and registration


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
            user_confirmation_token = ts.dumps(
                user_email, salt="confirm-email")
            # Have Flask generate an external link
            confirm_url = url_for('users.confirm_email',
                                  token=user_confirmation_token, _external=True)
            html = render_template(
                'users/mail/confirm_email.html', confirm_url=confirm_url, user=new_user)
            send_email("Please confirm your email",
                       recipients=[user_email], html=html)
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
        # max_age=86400 sets token to expire in one day
        user_email = ts.loads(token, salt="confirm-email", max_age=86400)
    except:
        # Abort if token is not valid
        abort(404)
    user = User.query.filter_by(email=user_email).first()
    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()
    # Log user in after email confirmed
    login_user(user)
    flash('Successfully confirmed email account.')
    return redirect(url_for('main.dashboard'))


@users.route('/resend-confirmation', methods=["GET", "POST"])
@anonymous_required('/dashboard')
def resend_confirmation():
    form = SendConfirmEmailForm(request.form)
    if request.method == "POST":
        user_email = form.data['email']
        user = User.query.filter_by(email=user_email).first()
        if user:
            if not user.email_confirmed:
                ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
                user_confirmation_token = ts.dumps(
                    user_email, salt="confirm-email")
                # Have Flask generate an external link
                confirm_url = url_for('users.confirm_email',
                                      token=user_confirmation_token, _external=True)
                html = render_template(
                    'users/mail/confirm_email.html', confirm_url=confirm_url, user=user)
                send_email("Please confirm your email",
                           recipients=[user_email], html=html)
                flash('Successfully resent account confirmation email.')
                return redirect(url_for('users.login'))
            else:
                flash('Email already confirmed.')
        else:
            flash('This email is not associated with an account.')
    return render_template('users/resend_confirmation.html', form=form)


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


# Settings and password changes


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
@anonymous_required('/dashboard')
def reset_password():
    form = SendResetEmailForm(request.form)
    if request.method == "POST":
        user_email = form.data['email']
        user = User.query.filter_by(email=user_email).first()
        if user:
            ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            user_reset_token = ts.dumps(user_email, salt="reset-password")
            # Have Flask generate an external link
            confirm_url = url_for(
                'users.reset_password_token', token=user_reset_token, _external=True)
            html = render_template(
                'users/mail/reset_password.html', confirm_url=confirm_url, user=user)
            send_email("Password reset request",
                       recipients=[user_email], html=html)
            flash('Successfully sent password reset email.')
            return redirect(url_for('users.login'))
        else:
            flash('This email is not associated with an account.')
    return render_template('users/reset_password.html', form=form)


@users.route('/reset-password/<token>', methods=["GET", "POST"])
@anonymous_required('/dashboard')
def reset_password_token(token):
    try:
        ts = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        # max_age=3600 sets token expiration to one hour
        user_email = ts.loads(token, salt="reset-password", max_age=3600)
    except:
        # Abort if token is not valid
        abort(404)
    form = ResetPasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=user_email).first()
        user.password = User.encrypt_password(form.data['new_password'])
        db.session.add(user)
        db.session.commit()
        # Log user in after password changed
        login_user(user)
        flash('Successfully reset password.')
        return redirect(url_for('main.dashboard'))
    return render_template('users/reset_password_token.html', form=form, token=token)
