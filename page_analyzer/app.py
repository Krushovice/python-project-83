import os
from page_analyzer.db import (add_check, add_url, get_page_by_id,
                              get_all_checks, get_check_page,
                              get_unique, get_url)
from dotenv import load_dotenv
from page_analyzer.utils import (is_valid, get_status,
                                 to_valid_string, normalize_simple,
                                 site_analize)
from flask import (Flask, flash, render_template, request,
                   redirect, url_for)


# конфигурация
load_dotenv()
app = Flask(__name__)

app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config.from_object(__name__)


@app.errorhandler(500)
def server_error(error):
    return render_template('error500.html')


@app.errorhandler(404)
def unprocessable(error):
    return render_template('error404.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def set_urls():
    url = request.form['url']
    if is_valid(url):
        addr = to_valid_string(url)
        if not add_url(addr):
            flash('Страница уже существует', category='success')

        else:
            flash('Страница успешно добавлена', category='success')
        db_page = get_url(addr)
        data = normalize_simple(db_page)
        page_id = data['id']
        return redirect(url_for('show_url', id=f'{page_id}'))
    else:
        flash('Некорректный URL', category='danger')
        return render_template('index.html'), 422


@app.route('/urls')
def get_urls():
    urls = get_unique()
    check_data = get_all_checks()
    return render_template('urls.html',
                           urls=urls,
                           check_data=check_data)


@app.route('/urls/<id>')
def show_url(id):
    db_data = get_page_by_id(id)
    page = normalize_simple(db_data)
    id = id
    name = page['name']
    date = page['date'].date()
    checks = get_check_page(id)
    return render_template('url_page.html',
                           id=id,
                           name=name,
                           date=date,
                           checks=checks)


@app.route('/urls/<id>/checks', methods=['POST', 'GET'])
def check_url(id):
    if request.method == "POST":
        db_page = get_page_by_id(id)
        url = normalize_simple(db_page)
        status = get_status(url['name'])
        if status != 200:
            flash("Произошла ошибка при проверке", category='danger')
            return redirect(url_for('show_url', id=id))

        data = site_analize(url['name'])
        add_check(id, data, status)
        flash('Страница успешно проверена', category='success')
        return redirect(url_for('show_url',
                                id=id))

    else:
        return render_template(url_for('show_url', id=id))
