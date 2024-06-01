from werkzeug.security import generate_password_hash

from app import db
from app.models import RepairWorker

def register_cli(app, db):
    @app.cli.command('create-admin')
    def create_admin():
        """Создание админ пользователя"""
        username = input('Введите имя пользователя: ')
        email = input('Введите email: ')
        hashed_password = generate_password_hash(input('Введите пароль: '))

        admin = RepairWorker(username=username, email=email, password_hash=hashed_password, is_admin=True)

        db.session.add(admin)
        db.session.commit()