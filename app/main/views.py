import uuid
from datetime import datetime

from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required

from app.models import User, RepairRequest
from app.forms import RegistrationForm, LoginForm, RepairRequestForm, SearchRepairRequestForm
from app import db, bcrypt


def get_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Ошибка в поле {getattr(form, field).label.text}: {error}", 'danger')


def calc_work_time(obj):
    return (obj.complete_at - obj.request_date).total_seconds()


def get_object(model: db.Model, pk: uuid.uuid4):
    response = db.session.get(model, str(pk))
    if not response:
        abort(404)
    return response


def home():
    return render_template('home/home.html')


def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
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
            flash('Invalid username or password.', 'danger')

    return render_template('registration/login.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_required
def profile():
    requests = RepairRequest.query.all()
    active_requests = [item for item in filter(lambda x: x.is_active, requests)]
    inactive_requests = [item for item in filter(lambda x: not x.is_active, requests)]
    repairmans = User.query.filter_by(is_repairman=True).all()

    total_work_time = sum(item for item in map(calc_work_time, inactive_requests))
    if inactive_requests:
        average_uptime_seconds = total_work_time / len(inactive_requests)
        average_uptime_hours = round(float(average_uptime_seconds / 3600), 3)
    else:
        average_uptime_hours = 0
    return render_template('profile/profile.html',
                           active_requests=active_requests,
                           history=requests,
                           inactive_requests=inactive_requests,
                           repairmans=repairmans,
                           create_request_form=RepairRequestForm(current_user),
                           search_request_form=SearchRepairRequestForm(),
                           average_uptime_hours=average_uptime_hours,
                           )


@login_required
def create_repair_request():
    form = RepairRequestForm(current_user)
    if form.validate_on_submit():
        request_date = datetime.now().date()
        request_date = request_date.replace(microsecond=0)
        if not form.current_master.data:
            flash('Вы не выбрали ремонтника', 'danger')
            return redirect(url_for('main.profile'))

        repair_request = RepairRequest(
            request_date=request_date,
            device_type=form.device_type.data,
            device_model=form.device_model.data,
            issue_description=form.issue_description.data,
            client_name=form.client_name.data,
            client_phone=form.client_phone.data,
            status=form.status.data,
            # is_active=form.is_active.data,
            current_master_id=form.current_master.data
        )
        db.session.add(repair_request)
        db.session.commit()
        flash('Запрос на ремонт создан', 'success')
        return redirect(url_for('main.profile'))

    get_errors(form)
    return redirect(url_for('main.profile'))


@login_required
def edit_repair_request(pk):
    repair_request = get_object(RepairRequest, pk)
    if not repair_request.is_active:
        abort(404)
    form = RepairRequestForm(current_user, obj=repair_request)

    if form.validate_on_submit():
        repair_request.device_type = form.device_type.data
        repair_request.device_model = form.device_model.data
        repair_request.issue_description = form.issue_description.data
        repair_request.current_master = form.current_master.data
        repair_request.client_name = form.client_name.data
        repair_request.client_phone = form.client_phone.data
        repair_request.status = form.status.data
        repair_request.master_comment = form.master_comment.data
        repair_request.is_active = form.is_active.data

        db.session.commit()
        return redirect(url_for('main.profile'))
    get_errors(form)
    return render_template('request/request_edit.html', form=form)


@login_required
def info_repair_request(pk):
    repair_request = get_object(RepairRequest, pk)
    return render_template('request/request_ifno.html', request=repair_request)

@login_required
def complete_repair_request(pk):
    repair_request = get_object(RepairRequest, pk)
    complete_date = datetime.now().replace(microsecond=0)

    repair_request.is_active = False
    repair_request.complete_at = complete_date
    db.session.commit()
    # flash(f'Заявка на ремонт {repair_request.id} выполнена.', 'success')
    return redirect(url_for('main.profile'))


@login_required
def search_results():
    form = SearchRepairRequestForm()
    if form.validate_on_submit():
        phone = form.client_phone.data
        search_term = f"%{phone}%"
        results = RepairRequest.query.filter(RepairRequest.client_phone.like(search_term)).all()
        if results:
            return render_template('profile/search_results.html', results=results, phone=phone)
        else:
            flash(f'Контакт с номером телефона {phone} не найден.', 'danger')
            return redirect(url_for('main.profile'))
    flash(f'Неверный формат номера телефона', 'danger')
    return redirect(url_for('main.profile'))
