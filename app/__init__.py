from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Настройка конфигурации
    app.config.from_object('config.Config')
    db.init_app(app)

    migrate = Migrate(app, db)


    with app.app_context():
        # Регистрация блюпринтов

        from .main.errors import errors as main_blueprint
        app.register_blueprint(main_blueprint)

        # Дополнительная инициализация, если требуется
        from .routes import register_routes
        register_routes(app, db)

    return app
