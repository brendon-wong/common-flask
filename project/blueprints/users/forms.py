from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=1, max=128)])
    preferred_name = StringField('Name to Address You By',
                                 validators=[DataRequired(), Length(min=1, max=128)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=3, max=265)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=128)])


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=3, max=265)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=128)])


class SettingsForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=1, max=128)])
    preferred_name = StringField('Name to Address You By',
                                 validators=[DataRequired(), Length(min=1, max=128)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=3, max=265)])
    password = PasswordField('Verify Password',
                             validators=[DataRequired(), Length(min=6, max=128)])


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Current Password',
                             validators=[DataRequired(), Length(min=6, max=128)])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(), Length(min=6, max=128)])


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(), Length(min=6, max=128)])
