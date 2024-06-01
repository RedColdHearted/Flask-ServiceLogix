from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app.models import RepairWorker, Manager
from app.forms import RegistrationForm, LoginForm
from app import db


def find_user_by_username(username):
    models = [RepairWorker, Manager]  # Добавь сюда все модели, с которыми ты работаешь
    for model in models:
        user = model.query.filter_by(username=username).first()
        if user:
            return user
    return None

def home():
    return render_template('home/home.html')


def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = RepairWorker(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))

    return render_template('registration/register.html', title='Register', form=form)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = find_user_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.')
    return render_template('registration/login.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))