import os
import psycopg2
from datetime import datetime
from page_analyzer.db import FDataBase
from dotenv import load_dotenv
from page_analyzer.validator import validate
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
            if not dbase.getUrl(url):
                data = dbase.addUrl(url)
                page_id = dbase.getIdAfterAdd(url)
                flash('Страница успешно добавлена',category='success')
                return redirect(url_for('show_url', id=f'{page_id}'))
            flash('Страница уже существует', category='success')
            page_id = dbase.getIdAfterAdd(url)
            return redirect(url_for('show_url', id=f'{page_id}'))
        else:
            flash('Некорректный URL', category='danger')
            return redirect(url_for('index'))


    else:
        data = dbase.getUnique()
        if data:
            return render_template('urls.html', data=data)

        return render_template('urls.html')
        # last_check = datetime.now().date()
        # content = render_template('urls.html', data=data, last_check=last_check)
        # status = make_response(content).status_code


@app.route('/urls/<id>')
def show_url(id):
    page = dbase.getPageById(id)
    print(page)
    return render_template('index.html')
    # id = id
    # name = page['name']
    # date = page['date']
    # return render_template('url_page.html',
    #                        id=id,
    #                        name=name,
    #                        date=date)


@app.route('/urls/<id>/checks', methods=['POST', 'GET'])
def check_url(id):
    if request.method == "POST":
        try:
            dbase.addCheck(id)
            page = dbase.getCheckPage(id)
            check_id = page['id']
            date_check = page['date']
            flash('Страница успешно проверена')
            return redirect(url_for('show_url', id=id),
                                    check_id=check_id,
                                    date_check=date_check)
        except psycopg2.Error as e:
            print('Ошибка проверки ' +str(e))

    else:
        return render_template(url_for('index'))

# @app.route('/urls/<id>/checks')
# def url_checks(id):
#     page = dbase.getPageById(id)
#     id = id
#     name = page[1]
#     date = datetime.now().date()
#     return render_template('checks.html',
#                             id=id,
#                             name=name,
#                             date=date)



# def main():
#     app.run(debug=True)


# if __name__ == '__main__':
#     main()
