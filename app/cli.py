from werkzeug.security import generate_password_hash

from app.models import User

def get_info():
    username = input('Введите имя пользователя: ')
    email = input('Введите email: ')
    hashed_password = generate_password_hash(input('Введите пароль: '))
    return username, email, hashed_password

def register_cli(app, db):
    @app.cli.command('create-admin')
    def create_admin():
        """Создание админ пользователя"""
        username, email, hashed_password = get_info()
        admin = User(username=username, email=email, password_hash=hashed_password, is_admin=True)

        db.session.add(admin)
        db.session.commit()

    @app.cli.command('create-manager')
    def create_manager():
        """Создание менеджера"""
        username, email, hashed_password = get_info()
        admin = User(username=username, email=email, password_hash=hashed_password, is_manager=True)

        db.session.add(admin)
        db.session.commit()

    @app.cli.command('create-repairman')
    def create_repairman():
        """Создание ремонтника"""
        username, email, hashed_password = get_info()
        admin = User(username=username, email=email, password_hash=hashed_password, is_repairman=True)

        db.session.add(admin)
        db.session.commit()
