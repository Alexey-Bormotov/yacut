from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import ALLOWED_SYMBOLS, get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()

    if URL_map.query.filter_by(original=data['url']).first() is not None:
        raise InvalidAPIUsage(
            f'Имя "{data["custom_id"]}" уже занято.')

    if URL_map.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            f'Имя "{data["custom_id"]}" уже занято.')

    for char in data['custom_id']:
        if char not in ALLOWED_SYMBOLS:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

    if len(data['custom_id']) > 16:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')

    url_map = URL_map(
        original=data['url'],
        short=data['custom_id']
    )

    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for('index_view', _external=True) + url_map.short
    }), 201
