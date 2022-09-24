from random import choices

from flask import Markup, abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map


ALLOWED_SYMBOLS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                   'abcdefghijklmnopqrstuvwxyz' +
                   '0123456789')


def get_unique_short_id():
    short_id = ''.join(choices(ALLOWED_SYMBOLS, k=6))

    while URL_map.query.filter_by(short=short_id).first():
        short_id = ''.join(choices(ALLOWED_SYMBOLS, k=6))

    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        original = URL_map.query.filter_by(original=original_link).first()
        if original:
            flash(f'Имя {custom_id} уже занято!')

            return render_template('index.html', form=form)

        short = URL_map.query.filter_by(short=custom_id).first()
        if short:
            flash(f'Имя {custom_id} уже занято!')

            return render_template('index.html', form=form)

        if custom_id:
            for char in custom_id:
                if char not in ALLOWED_SYMBOLS:
                    flash('Недопустимые символы! ' +
                          'Разрешены только большие и маленькие латинские ' +
                          'буквы и цифры в диапазоне 0-9')

                    return render_template('index.html', form=form)
        else:
            custom_id = get_unique_short_id()

        url_map = URL_map(
            original=original_link,
            short=custom_id,
        )

        db.session.add(url_map)
        db.session.commit()

        result_url = url_for('index_view', _external=True) + url_map.short

        flash(Markup(
            f'Ваша новая ссылка готова: '
            f'<a href="{result_url}">'
            f'{result_url}</a>'
        )
        )

    return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()

    if url_map:
        return redirect(url_map.original)

    abort(404)
