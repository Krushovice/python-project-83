import functools
import psycopg2
import logging
from psycopg2 import extras
from flask import current_app as app
from datetime import datetime


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


# создаем декоратор для управления подключением и закрытием сессии с БД
def with_database_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(app.config['DATABASE_URL'])
            result = func(conn, *args, **kwargs)
        except psycopg2.Error as e:
            logging.error(f"Ошибка работы с БД: {e}")
            result = None
        finally:
            if conn:
                conn.close()
        return result
    return wrapper


@with_database_connection
def add_url(conn, addr):
    with conn.cursor() as cur:
        tm = datetime.now()
        cur.execute('SELECT id FROM urls WHERE name = %s', (addr,))
        existing_record = cur.fetchone()

        if existing_record:
            logging.error('Запись с таким именем уже существует')
            return False

        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (addr, tm))
        conn.commit()
        return True
    return False


@with_database_connection
def add_check(conn, id, data, status):
    with conn.cursor() as cur:
        tm = datetime.now()
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

    return False


@with_database_connection
def get_check_page(conn, url_id):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
        cur.execute("""SELECT *
                       FROM url_checks
                       WHERE url_id = %s
                       ORDER BY id DESC""", (url_id,))
        res = cur.fetchall()
        if not res:
            logging.error('Проверка не найдена')
            return False
        return res

    return False


@with_database_connection
def get_page_by_id(conn, url_id):
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM urls
                       WHERE id = %s LIMIT 1""", (url_id,))
        res = cur.fetchone()
        if not res:
            logging.error('Cайт не найден')
            return False
        return res

    return False


@with_database_connection
def get_url(conn, url):
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM urls
                       WHERE name = %s""", (url,))
        res = cur.fetchone()
        if not res:
            logging.error('Cайт не найден')
            return False
        return res
    return False


@with_database_connection
def get_unique(conn):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
        cur.execute("""SELECT * FROM urls
                       ORDER BY created_at DESC
                       LIMIT 5""")
        res = cur.fetchall()
        if not res:
            logging.error('Таблица пуста')
            return False
        return res

    return False


@with_database_connection
def get_all_checks(conn):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cur:
        cur.execute("""SELECT * FROM url_checks
                       ORDER BY id DESC
                       LIMIT 5""")
        res = cur.fetchall()

        if not res:
            logging.error('Таблица пуста')
            return False
        return res

    return False
