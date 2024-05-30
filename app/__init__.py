from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Настройка конфигурации
    app.config.from_object('config.Config')
    db.init_app(app)

    login_manager.init_app(app)
    bcrypt = Bcrypt(app)

    migrate = Migrate(app, db)

    with app.app_context():
        # Регистрация блюпринтов

        from .main.errors import errors as main_blueprint
        app.register_blueprint(main_blueprint)

        # Дополнительная инициализация, если требуется
        from .routes import register_routes
        register_routes(app, db)

    return app
