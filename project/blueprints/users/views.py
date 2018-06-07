"""User blueprint."""
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from project.extensions import db
from project.blueprints.users.decorators import anonymous_required, roles_required
from project.blueprints.users.forms import UserForm, LoginForm
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
        except IntegrityError as e:
            flash("Email address already in use.")
            return render_template('users/register.html', form=form)
        flash('Successfully created account.')
        return redirect(url_for('main.dashboard'))
    return render_template('users/register.html', form=form)


@users.route('/login', methods=["GET", "POST"])
@anonymous_required('/dashboard')
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(
                form.data['email'], form.data['password'])
            if user:
                login_user(user)
                flash("Successfully logged in.")
                return redirect(url_for('main.dashboard'))
        flash("Invalid Credentials")
    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('users.login'))
