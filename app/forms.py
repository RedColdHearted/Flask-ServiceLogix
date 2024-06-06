import re

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from .models import User
from .schemas import RepairRequestStatus


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


class PhoneFormMixin:
    phone_pattern = r'^[\d\(\)\-\s]+$'  # Регулярное выражение для разрешенных символов в номере телефона
    client_phone = StringField('Телефон клиента', validators=[DataRequired(), Length(max=20), Regexp(phone_pattern,
                                                                                                     message="Некорректный номер телефона")])


class RepairRequestForm(FlaskForm, PhoneFormMixin):
    device_type = StringField('Тип устройства', validators=[DataRequired(), Length(max=50)])
    device_model = StringField('Модель устройства', validators=[DataRequired(), Length(max=50)])
    issue_description = TextAreaField('Описание проблемы', validators=[DataRequired()])
    client_name = StringField('Имя клиента', validators=[DataRequired(), Length(max=100)])
    is_active = BooleanField('Активный запрос')


class EditRepairRequestForm(FlaskForm, PhoneFormMixin):
    device_type = StringField('Тип устройства', validators=[DataRequired(), Length(max=50)])
    device_model = StringField('Модель устройства', validators=[DataRequired(), Length(max=50)])
    issue_description = TextAreaField('Описание проблемы', validators=[DataRequired()])
    client_name = StringField('Имя клиента', validators=[DataRequired(), Length(max=100)])
    status = SelectField('Статус', choices=[(status.name, status.value) for status in RepairRequestStatus])
    master_comment = TextAreaField('Комментарий мастера', validators=[Length(max=200)])
    is_active = BooleanField('Активный запрос')


class SearchRepairRequestForm(FlaskForm, PhoneFormMixin):
    pass
