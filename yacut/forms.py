from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import ValidationError, DataRequired, Length, Optional, URL

from settings import ALLOWED_SYMBOLS, MAX_SHORT_ID_SIZE, MAX_URL_SIZE


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Введите корректный URL адрес'),
                    Length(max=MAX_URL_SIZE)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=MAX_SHORT_ID_SIZE),
                    Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        for char in self.custom_id.data:
            if char not in ALLOWED_SYMBOLS:
                raise ValidationError(
                    f'Символ {char} недопустим в короткой ссылке.')
