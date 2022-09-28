from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import URLForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    data = {
        'original': form.original_link.data,
        'short': form.custom_id.data
    }

    if URL_map.url_map_is_exist(data):
        flash(f'Имя {data["short"]} уже занято!')

        return render_template('index.html', form=form)

    url_map = URL_map.create_url_map(data)
    flash('Ваша новая ссылка готова:')

    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url_map.short
    )


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    url_map = URL_map.get_url_map(short_id)

    if url_map:
        return redirect(url_map.original)

    abort(404)
