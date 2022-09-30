import os
import re
from string import ascii_letters, digits


ALLOWED_SYMBOLS = ascii_letters + digits
REGEXP = r'[' + re.escape(ALLOWED_SYMBOLS) + r']+'
MAX_URL_SIZE = 2048
MAX_SHORT_ID_SIZE = 16
DEFAULT_SHORT_ID_SIZE = 6
GENERATE_SHORT_ID_TRIES = 5


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'MY_SECRET_KEY')
