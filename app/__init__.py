from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

from app.admin import create_admin

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
socketio = SocketIO()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Настройка конфигурации
    app.config.from_object('config.Config')
    db.init_app(app)

    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    migrate = Migrate(app, db)
    socketio.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # Регистрация блюпринтов

        from .main.errors import errors as errors_blueprint
        app.register_blueprint(errors_blueprint)

        # Дополнительная инициализация, если требуется
        from .routes import register_routes
        register_routes(app, db)

        from app.cli import register_cli
        register_cli(app, db)

    create_admin(app)

    return app
