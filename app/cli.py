from werkzeug.security import generate_password_hash

from app.models import User

def register_cli(app, db):
    @app.cli.command('create-admin')
    def create_admin():
        """Создание админ пользователя"""
        username = input('Введите имя пользователя: ')
        email = input('Введите email: ')
        hashed_password = generate_password_hash(input('Введите пароль: '))

        admin = User(username=username, email=email, password_hash=hashed_password, is_admin=True)

        db.session.add(admin)
        db.session.commit()

    @app.cli.command('create-manager')
    def create_manager():
        """Создание менеджера"""
        username = input('Введите имя пользователя: ')
        email = input('Введите email: ')
        hashed_password = generate_password_hash(input('Введите пароль: '))

        admin = User(username=username, email=email, password_hash=hashed_password, is_manager=True)

        db.session.add(admin)
        db.session.commit()
