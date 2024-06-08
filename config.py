import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://chiefbiefkief:maxim2005@chiefbiefkief.mysql.pythonanywhere-services.com/chiefbiefkief$default')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching for static files
