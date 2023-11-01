import functools
import psycopg2
from flask import current_app as app
from datetime import datetime
from page_analyzer.validator import (toValidString, normalizeNested,
                                     normalizeSimple, siteAnalize)


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
def addUrl(conn, url):
    try:
        with conn.cursor() as cur:
            tm = datetime.now()
            addr = toValidString(url)
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
def addCheck(conn, id, status):
    try:
        with conn.cursor() as cur:
            tm = datetime.now()
            url = getPageById(id)
            data = siteAnalize(url['name'])
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
def getCheckPage(conn, url_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT *
                           FROM url_checks
                           WHERE url_id = %s
                           ORDER BY id DESC""", (url_id,))
            res = cur.fetchall()
            if not res:
                print('Проверка не найдена')
                return False
            return normalizeNested(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def getPageById(conn, url_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM urls
                           WHERE id = %s LIMIT 1""", (url_id,))
            res = cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalizeSimple(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def getUrl(conn, url):
    try:
        with conn.cursor() as cur:
            url = toValidString(url)
            cur.execute("""SELECT * FROM urls
                           WHERE name = %s""", (url,))
            res = cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalizeSimple(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД ' + str(e))
        return False


@with_database_connection
def getUnique(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM urls
                           ORDER BY created_at DESC
                           LIMIT 5""")
            res = cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return normalizeNested(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False


@with_database_connection
def getAllChecks(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM url_checks
                           ORDER BY id DESC
                           LIMIT 5""")
            res = cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return normalizeNested(res)
    except psycopg2.Error as e:
        print('Ошибка получения данных из БД: ' + str(e))
        return False
