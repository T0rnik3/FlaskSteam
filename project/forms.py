from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from project.models import User


class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        if user := User.query.filter_by(username=username_to_check.data).first():
            raise ValidationError('Username already exists! Please try a different username')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class AddGameForm(FlaskForm):
    submit = SubmitField(label='Add to your Wishlist!')

class RemoveGameForm(FlaskForm):
    submit = SubmitField(label='Confirm to Remove!')


class UpdateAccountForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        if username_to_check.data != current_user.username:
            if user := User.query.filter_by(username=username_to_check.data).first():
                raise ValidationError('Username already exists! Please try a different username')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Update')


class UpdatePasswordForm(FlaskForm):
    
    old_password = PasswordField(label='Old Password:', validators=[DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Update')
