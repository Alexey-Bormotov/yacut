from flask import abort, flash, redirect, render_template, url_for

from . import app
from .error_handlers import GenerationError
from .forms import URLForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original, short = form.original_link.data, form.custom_id.data
    if URL_map.get_url_map(short):
        flash(f'Имя {short} уже занято!')
        return render_template('index.html', form=form)
    if (short != '' and
       short is not None and
       not URL_map.short_id_is_correct(short)):
        flash('Указано недопустимое имя для короткой ссылки')
        return render_template('index.html', form=form)
    try:
        url_map = URL_map.create_url_map(original, short)
    except GenerationError:
        abort(500)
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
