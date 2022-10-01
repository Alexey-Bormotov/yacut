from datetime import datetime
from random import choices
import re
from urllib.parse import urlparse

from . import db
from .error_handlers import GenerationError
from settings import (ALLOWED_SYMBOLS, DEFAULT_SHORT_ID_SIZE,
                      GENERATE_SHORT_ID_TRIES, MAX_SHORT_ID_SIZE, MAX_URL_SIZE,
                      REGEXP)


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        for _ in range(GENERATE_SHORT_ID_TRIES):
            short_id = ''.join(choices(
                ALLOWED_SYMBOLS,
                k=DEFAULT_SHORT_ID_SIZE)
            )
            if not URL_map.get_url_map(short_id):
                return short_id
        raise GenerationError('Не удалось сгенерировать уникальную ссылку')

    @staticmethod
    def validate_url(url):
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    @staticmethod
    def url_is_correct(url):
        return len(url) < MAX_URL_SIZE and URL_map.validate_url(url)

    @staticmethod
    def validate_short_id(short_id):
        match = re.match(REGEXP, short_id)
        return match is not None and match.group() == short_id

    @staticmethod
    def short_id_is_correct(short_id):
        return (len(short_id) < MAX_SHORT_ID_SIZE and
                URL_map.validate_short_id(short_id))

    @staticmethod
    def create_url_map(original, short):
        if not short:
            short = URL_map.get_unique_short_id()
        url_map = URL_map(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_url_map(short_id):
        return URL_map.query.filter_by(short=short_id).first()
