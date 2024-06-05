from datetime import datetime

from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app.models import User, RepairRequest
from app.forms import RegistrationForm, LoginForm, RepairRequestForm
from app import db


def home():
    return render_template('home/home.html')


def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, is_repairmain=True)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))

    return render_template('registration/register.html', title='Register', form=form)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password.')
    return render_template('registration/login.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_required
def profile():
    requests = RepairRequest.query.all()
    active_requests = [item for item in filter(lambda x: x.is_active, requests)]
    repairmans = User.query.filter_by(is_repairman=True).all()
    return render_template('profile/profile.html',
                           active_requests=active_requests,
                           history=requests,
                           repairmans=repairmans,
                           create_request_form=RepairRequestForm(),
                           )

@login_required
def create_repair_request():
    form = RepairRequestForm()
    if form.validate_on_submit():
        request_date = datetime.utcnow()
        request_date = request_date.replace(microsecond=0)
        repair_request = RepairRequest(
            request_date=request_date,
            device_type=form.device_type.data,
            device_model=form.device_model.data,
            issue_description=form.issue_description.data,
            client_name=form.client_name.data,
            client_phone=form.client_phone.data,
            is_active=form.is_active.data,
            current_master_id=current_user.id  # Берем из текущего пользователя
        )
        db.session.add(repair_request)
        db.session.commit()
        flash('Запрос на ремонт создан', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile/profile.html', form=form)
