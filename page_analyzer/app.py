import os
import psycopg2
# from .db import FDataBase
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
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# def get_db():
#     if not hasattr(g, 'link_db'):
#         g.link_db = connect_db()
#     return g.link_db


# dbase = None


# @app.before_request
# def before_request():
#     global dbase

#     db = get_db()
#     dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    return render_template('urls.html')


@app.route('/urls', method = 'POST')
def check_url():
    pass

@app.route('/urls/<id>')
def show_url(id):
    pass


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
