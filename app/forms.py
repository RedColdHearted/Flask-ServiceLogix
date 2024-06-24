from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from app.database.models import User
from app.database.schemas import RepairRequestStatus


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
    client_phone = StringField('Телефон клиента',
                               validators=[DataRequired(), Length(min=11, max=11),
                                           Regexp(phone_pattern, message="Некорректный номер телефона")]
                               )


class RepairRequestForm(FlaskForm, PhoneFormMixin):
    device_type = StringField('Тип устройства', validators=[DataRequired(), Length(max=50)])
    device_model = StringField('Модель устройства', validators=[DataRequired(), Length(max=50)])
    issue_description = TextAreaField('Описание проблемы', validators=[DataRequired()])
    client_name = StringField('Имя клиента', validators=[DataRequired(), Length(max=100)])
    status = SelectField('Статус', choices=[(status.name, status.value) for status in RepairRequestStatus])
    master_comment = TextAreaField('Комментарий мастера', validators=[Length(max=200)])
    is_active = BooleanField('Активный запрос')

    current_master = SelectField('Мастер', coerce=str)  # добавленное поле для выбора мастера

    def __init__(self, current_user, *args, **kwargs):
        super(RepairRequestForm, self).__init__(*args, **kwargs)
        if current_user.is_manager or current_user.is_admin:
            self.current_master.choices = [
                                              ('', 'Не выбрано')] + [
                                              (repairman.id, repairman.username) for repairman in
                                              User.query.filter_by(is_repairman=True).all()
                                          ]
        else:
            # Установка текущего пользователя в качестве мастера по умолчанию
            self.current_master.choices = [(current_user.id, current_user.username)]
            self.current_master.data = current_user.id  # Значение по умолчанию
            self.current_master.render_kw = {'disabled': 'disabled'}  # Отключаем поле для редактирования


class SearchRepairRequestForm(FlaskForm, PhoneFormMixin):
    pass
