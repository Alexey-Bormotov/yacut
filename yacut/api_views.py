import re
from urllib.parse import urlparse

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URL_map

from settings import ALLOWED_SYMBOLS, MAX_SHORT_ID_SIZE, MAX_URL_SIZE


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.get_url_map(short_id)

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

    if len(data['url']) > MAX_URL_SIZE:
        raise InvalidAPIUsage(
            'Превышена допустимая длина URL')

    parsed_url = urlparse(data['url'])
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise InvalidAPIUsage(
            'Введите корректный URL адрес')

    if ('custom_id' not in data or
       data['custom_id'] is None or
       data['custom_id'] == ''):

        data['custom_id'] = URL_map.get_unique_short_id()

    data = {
        'original': data['url'],
        'short': data['custom_id']
    }

    if URL_map.url_map_is_exist(data):
        raise InvalidAPIUsage(
            f'Имя "{data["short"]}" уже занято.')

    regexp = r'[' + ALLOWED_SYMBOLS + r']+'
    match = re.match(regexp, data['short'])
    if match is None or match.group() != data['short']:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')

    if len(data['short']) > MAX_SHORT_ID_SIZE:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')

    url_map = URL_map.create_url_map(data)

    return jsonify({
        'url': url_map.original,
        'short_link': url_for('index_view', _external=True) + url_map.short
    }), 201
