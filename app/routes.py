from flask import Blueprint

from .main.views import home, login, register, logout, profile

main = Blueprint('main', __name__)


def register_routes(app, db):
    main.add_url_rule('/', 'home', home)
    main.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    main.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
    main.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    main.add_url_rule('/profile', 'profile', profile)

    app.register_blueprint(main)
