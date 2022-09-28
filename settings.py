import os
from string import ascii_letters, digits

ALLOWED_SYMBOLS = ascii_letters + digits
MAX_URL_SIZE = 512
MAX_SHORT_ID_SIZE = 16
DEFAULT_SHORT_ID_SIZE = 6


class Config(object):
    # С другим именем по умолчанию не проходит тест
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'MY_SECRET_KEY')
