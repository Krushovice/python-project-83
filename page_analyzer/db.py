import math
from datetime import datetime
import psycopg2
import psycopg2.extras
from flask import url_for
from page_analyzer.validator import parseUrl, normalize_str, normalize


class FDataBase:
    def __init__(self, db):
        self.__db = db
        # self.__cur = db.cursor()
        self.__dict_cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    def addUrl(self, url):
        try:
            tm = datetime.now()
            addr = parseUrl(url)
            self.__dict_cur.execute('SELECT id FROM urls WHERE name = %s', (addr,))
            existing_record = self.__dict_cur.fetchone()

            if existing_record:
                print('Запись с таким именем уже существует')
                return False
            self.__dict_cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (addr, tm))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления адреса в БД "+str(e))
            return False
        return True

    def addCheck(self, id):
        try:
            tm = datetime.now()
            url_id = id
            # addr = parseUrl(url)
            self.__dict_cur.execute('INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)', (url_id, tm))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления записи в БД "+str(e))
            return False
        return True

    def getCheckPage(self, url_id):
        try:
            self.__dict_cur.execute(f"""SELECT *
                                  FROM url_checks
                                  WHERE url_id = {url_id}
                                  ORDER BY id
                                  DESC
                                  LIMIT 1""")
            res = self.__dict_cur.fetchone()
            if not res:
                print('Проверка не найдена')
                return False
            return normalize(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getPageById(self, url_id):

        try:
            self.__dict_cur.execute(f"""SELECT * FROM urls
                                WHERE id = {url_id} LIMIT 1""")

            res = self.__dict_cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False

            return normalize(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getUrl(self, url):
        try:
            self.__dict_cur.execute("""SELECT * FROM urls
                                WHERE name = %s""", (url,))
            res = self.__dict_cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalize(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД '+str(e))

        return False

    def getIdAfterAdd(self, url):
        # Вызываем метод getUrl для получения данных после добавления
        data = self.getUrl(url)
        if data:
            # Если данные найдены, возвращаем id из полученных данных
            return data['id']
        else:
            return None

    def getUnique(self):
        try:
            self.__dict_cur.execute("""SELECT * FROM urls ORDER BY created_at DESC LIMIT 5""")
            res = self.__dict_cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))
            return False

    def getAllChecks(self):
        try:
            self.__dict_cur.execute("""SELECT * FROM url_checks ORDER BY id DESC LIMIT 5""")
            res = self.__dict_cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))
            return False
