from flask import request, render_template, jsonify, Blueprint
from flask import request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models import RepairRequest, RepairRequestStatus, RepairWorker
from app.schemas import RepairRequestCreate, RepairRequestResponse, RepairRequestUpdateStatus
from .main.views import home, login, register, logout

main = Blueprint('main', __name__)

def register_routes(app, db):
    main.add_url_rule('/', 'home', home)
    main.add_url_rule('/login', 'login', login)
    main.add_url_rule('/logout', 'logout', logout)
    main.add_url_rule('/register', 'register', register)

    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(ModelView(RepairWorker, db.session))

    app.register_blueprint(main)