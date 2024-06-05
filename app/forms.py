from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

class RepairRequestForm(FlaskForm):
    device_type = StringField('Тип устройства', validators=[DataRequired(), Length(max=50)])
    device_model = StringField('Модель устройства', validators=[DataRequired(), Length(max=50)])
    issue_description = TextAreaField('Описание проблемы', validators=[DataRequired()])
    client_name = StringField('Имя клиента', validators=[DataRequired(), Length(max=100)])
    client_phone = StringField('Телефон клиента', validators=[DataRequired(), Length(max=20)])
    is_active = BooleanField('Активный запрос')
