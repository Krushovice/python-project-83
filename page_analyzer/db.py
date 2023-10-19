import math
from datetime import datetime
import psycopg2
from flask import url_for
from page_analyzer.validator import parseUrl


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUrl(self, url):
        try:
            tm = datetime.now()
            addr = parseUrl(url)
            self.__cur.execute('SELECT id FROM urls WHERE name = %s', (addr,))
            existing_record = self.__cur.fetchone()

            if existing_record:
                print('Запись с таким именем уже существует')
                return False
            self.__cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (addr, tm))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def getPageById(self, url_id):

        try:
            self.__cur.execute(f"""SELECT * FROM urls
                                WHERE id = {url_id} LIMIT 1 """)

            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False

            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getUrl(self, url):
        try:
            self.__cur.execute("""SELECT * FROM urls
                                WHERE name = %s""", (url,))
            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД '+str(e))

        return False

    def getIdAfterAdd(self, url):
        # Вызываем метод getUrl для получения данных после добавления
        data = self.getUrl(url)
        if data:
            # Если данные найдены, возвращаем id из полученных данных
            return data[0]
        else:
            return None

    def getUnique(self):
        try:
            self.__cur.execute("""SELECT * FROM urls ORDER BY created_at DESC LIMIT 5""")
            res = self.__cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))
            return False
