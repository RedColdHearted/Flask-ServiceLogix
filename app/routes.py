from flask import Blueprint

from .main.views import home, login, register, logout, profile, create_repair_request, edit_repair_request, \
    info_repair_request

main = Blueprint('main', __name__)


def register_routes(app, db):
    main.add_url_rule('/', 'home', home)
    main.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    main.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
    main.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    main.add_url_rule('/profile', 'profile', profile)

    main.add_url_rule('/create_repair_request', 'create_repair_request', create_repair_request,  methods=['GET', 'POST'])
    main.add_url_rule('/profile/edit-request/<uuid:pk>', 'edit_repair_request', edit_repair_request, methods=['GET', 'POST'])
    main.add_url_rule('/profile/info-request/<uuid:pk>', 'info_repair_request', info_repair_request, methods=['GET', 'POST'])

    app.register_blueprint(main)
