from flask import Blueprint
from werkzeug.security import generate_password_hash

from app.models import RepairWorker
from .main.views import home, login, register, logout

main = Blueprint('main', __name__)

def register_routes(app, db):
    main.add_url_rule('/', 'home', home)
    main.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    main.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
    main.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])

    app.register_blueprint(main)

    @app.cli.command('create-admin')
    def create_admin():
        """Создание админ пользователя. я не знаю куда это поместить"""
        username = input('Введите имя пользователя: ')
        email = input('Введите email: ')
        hashed_password = generate_password_hash(input('Введите пароль: '))

        admin = RepairWorker(username=username, email=email, password_hash=hashed_password, is_admin=True)

        db.session.add(admin)
        db.session.commit()