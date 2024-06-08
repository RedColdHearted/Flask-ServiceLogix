import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://username:password@localhost/dbname')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching for static files
