from flask import request, render_template, jsonify, Blueprint
from flask import request, jsonify
from app.models import RepairRequest, RepairRequestStatus
from app.schemas import RepairRequestCreate, RepairRequestResponse, RepairRequestUpdateStatus
from .main.views import home

main = Blueprint('main', __name__)

def register_routes(app, db):
    main.add_url_rule('/', 'home', home)
    # main.add_url_rule('/register', 'register', home)
    # main.add_url_rule('/login', 'login', home)

    app.register_blueprint(main)