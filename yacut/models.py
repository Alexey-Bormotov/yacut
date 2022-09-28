from datetime import datetime
from random import choices

from . import db

from settings import ALLOWED_SYMBOLS, DEFAULT_SHORT_ID_SIZE


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        short_id = None
        # Генерируем short_id до тех пор, пока не получим уникальный
        while URL_map.get_url_map(short_id) or short_id is None:
            short_id = ''.join(choices(ALLOWED_SYMBOLS, k=DEFAULT_SHORT_ID_SIZE))

        return short_id

    @staticmethod
    def url_map_is_exist(data):
        if (URL_map.query.filter_by(original=data['original']).first() or
           URL_map.query.filter_by(short=data['short']).first()):
            return True
        return False

    @staticmethod
    def create_url_map(data):
        if not data['short'] or data['short'] is None:
            data['short'] = URL_map.get_unique_short_id()

        url_map = URL_map(
            original=data['original'],
            short=data['short']
        )

        db.session.add(url_map)
        db.session.commit()

        return url_map

    @staticmethod
    def get_url_map(short_id):
        return URL_map.query.filter_by(short=short_id).first()
