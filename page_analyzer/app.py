import os
import psycopg2
import requests
from page_analyzer.db import FDataBase
from dotenv import load_dotenv
from page_analyzer.validator import validate
from flask import (Flask, flash, render_template, request,
                   redirect, url_for, g)


# конфигурация
load_dotenv()
app = Flask(__name__)

app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config.from_object(__name__)


# Подключение к базе данных
def connect_db():
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect(app.config['DATABASE_URL'])
    except psycopg2.Error as e:
        # в случае сбоя подключения будет выведено сообщение  в STDOUT
        print('Сбой подключения к БД: ' + str(e))
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    db = get_db()
    g.dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    if request.method == 'POST':
        url = request.form['url']
        if validate(url):
            if not g.dbase.addUrl(url):
                flash('Страница уже существует', category='success')
                data = g.dbase.getUrl(url)
                page_id = data['id']
                return redirect(url_for('show_url', id=f'{page_id}'))
            else:
                data = g.dbase.getUrl(url)
                page_id = data['id']
                flash('Страница успешно добавлена', category='success')
                return redirect(url_for('show_url', id=f'{page_id}'))

        else:
            flash('Некорректный URL', category='danger')
            return redirect(url_for('index'))

    else:
        urls = g.dbase.getUnique()
        if urls:
            check_data = g.dbase.getAllChecks()
            return render_template('urls.html',
                                   urls=urls,
                                   check_data=check_data)

        return render_template('urls.html')


@app.route('/urls/<id>')
def show_url(id):
    page = g.dbase.getPageById(id)
    id = id
    name = page['name']
    date = page['date'].date()
    checks = g.dbase.getCheckPage(id)
    return render_template('url_page.html',
                           id=id,
                           name=name,
                           date=date,
                           checks=checks)


@app.route('/urls/<id>/checks', methods=['POST', 'GET'])
def check_url(id):
    if request.method == "POST":
        page = g.dbase.getPageById(id)
        url = page['name']
        try:
            r = requests.get(url)
            status = r.status_code
        except psycopg2.Error as e:
            flash("Произошла ошибка при проверке", category='danger')
            print('Ошибка проверки ' + str(e))

        try:
            g.dbase.addCheck(id, status)
            flash('Страница успешно проверена', category='success')
            return redirect(url_for('show_url',
                                    id=id))

        except psycopg2.Error as e:
            print('Ошибка проверки ' + str(e))

    else:
        return render_template(url_for('show_url', id=id))
