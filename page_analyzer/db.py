import functools
import psycopg2
from psycopg2 import extras
from flask import current_app as app
from datetime import datetime
from page_analyzer.utils import (to_valid_string,
                                     normalize_simple,
                                     site_analize)


# создаем декоратор для управления подключением и закрытием сессии с БД
def with_database_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(app.config['DATABASE_URL'])
            result = func(conn, *args, **kwargs)
        except psycopg2.Error as e:
            print(f"Ошибка работы с БД: {e}")
            result = None
        finally:
            if conn:
                conn.close()
        return result
    return wrapper


@with_database_connection
def add_url(conn, url):
    try:
        with conn.cursor() as cur:
            tm = datetime.now()
            addr = to_valid_string(url)
            cur.execute('SELECT id FROM urls WHERE name = %s', (addr,))
            existing_record = cur.fetchone()

            if existing_record:
                print('Запись с таким именем уже существует')
                return False

            cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (addr, tm))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print("Ошибка добавления адреса в БД " + str(e))
        return False


@with_database_connection
def add_check(conn, id, status):
    try:
        with conn.cursor() as cur:
            tm = datetime.now()
            url = get_page_by_id(id)
            data = site_analize(url['name'])
            h1 = data['h1']
            title = data['title']
            description = data['description']

            url_id = id
            status_code = status
            cur.execute("""INSERT INTO url_checks
                           (url_id, status_code, h1, title,
                            description, created_at)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (url_id, status_code, h1, title, description, tm))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print("Ошибка добавления записи в БД " + str(e))
        return False


@with_database_connection
def get_check_page(conn, url_id):
    try:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("""SELECT *
                           FROM url_checks
                           WHERE url_id = %s
                           ORDER BY id DESC""", (url_id,))
            res = cur.fetchall()
            if not res:
                print('Проверка не найдена')
                return False
            return res
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def get_page_by_id(conn, url_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM urls
                           WHERE id = %s LIMIT 1""", (url_id,))
            res = cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalize_simple(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def get_url(conn, url):
    try:
        with conn.cursor() as cur:
            url = to_valid_string(url)
            cur.execute("""SELECT * FROM urls
                           WHERE name = %s""", (url,))
            res = cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalize_simple(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД ' + str(e))
        return False


@with_database_connection
def get_unique(conn):
    try:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("""SELECT * FROM urls
                           ORDER BY created_at DESC
                           LIMIT 5""")
            res = cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return res
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def get_all_checks(conn):
    try:
        with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
            cur.execute("""SELECT * FROM url_checks
                           ORDER BY id DESC
                           LIMIT 5""")
            res = cur.fetchall()

            if not res:
                print('Таблица пуста')
                return False
            return res
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False
