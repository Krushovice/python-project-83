import os
import psycopg2
from datetime import datetime
from db import FDataBase
from dotenv import load_dotenv
from validator import validate
from flask import (Flask, flash, render_template, request,
                   redirect, url_for, get_flashed_messages,
                   make_response, session, abort, g)


# конфигурация
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config.from_object(__name__)


# Подключение к базе данных
def connect_db():
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect(DATABASE_URL)
    except:
        # в случае сбоя подключения будет выведено сообщение  в STDOUT
        print('Сбой подключения к БД')
    return conn


def create_db():
    # Вспомогательная функция для создания таблиц БД
    db = connect_db()
    with app.open_resource('../database.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase

    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def get_urls():
    if request.method == 'POST':
        url = request.form['url']
        if validate(url):
            flash('Страница успешно добавлена',category='success')
            data = dbase.addUrl(url)
            return redirect(url_for('show_url', id=dbase.getIdAfterAdd(url)))
        else:
            flash('Некорректный URL', category='error')
            return redirect(url_for('index'))


    else:
        data = dbase.getUnique()
        return render_template('urls.html', data=data)

        # last_check = datetime.now().date()
        # content = render_template('urls.html', data=data, last_check=last_check)
        # status = make_response(content).status_code


@app.route('/urls/<id>')
def show_url(id):
    page = dbase.getPageById(id)
    id = page[0]
    name = page[1]
    created_at = page[2].date()

    if not page:
        abort(404)

    return render_template('check.html',
                           id=id,
                           name=name,
                           created_at=created_at)



def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
