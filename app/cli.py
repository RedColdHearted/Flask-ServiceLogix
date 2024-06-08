from app import bcrypt
from app.models import User


def get_info():
    username = input('Введите имя пользователя: ')
    email = input('Введите email: ')
    hashed_password = (input('Введите пароль: '))
    hashed_password = bcrypt.generate_password_hash(hashed_password).decode('utf-8')
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

    @app.cli.command('show-all-users')
    def show_all_users():
        users = User.query.all()
        headers = ["Username", "Email", "Is Admin", "Is Manager", "Is Repairman"]
        data = [(user.username, user.email, user.is_admin, user.is_manager, user.is_repairman) for user in users]
        column_widths = [max(len(str(item)) for item in column) for column in zip(*data)]
        column_widths = [max(len(header), width) for header, width in zip(headers, column_widths)]
        format_str = " | ".join([f"{{:<{width}}}" for width in column_widths])
        print('\n', format_str.format(*headers))
        print('-' * (sum(column_widths) + 3 * (len(headers) - 1)))
        for row in data:
            print(format_str.format(*row))
