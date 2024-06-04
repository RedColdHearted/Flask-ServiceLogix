from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app.models import User
from app.forms import RegistrationForm, LoginForm
from app import db


def home():
    return render_template('home/home.html')


def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, is_repairmain=True, template_name='perairman-profile')
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
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.')
    return render_template('registration/login.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_required
def profile():
    # TODO: переделать логику под одну страницу
    profile_template = 'profile/' + current_user.template_name + '.html'
    return render_template(profile_template)
