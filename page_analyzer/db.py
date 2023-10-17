import math
from datetime import datetime
import psycopg2
import re
from flask import url_for
from validator import parseUrl


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUrl(self, url):
        try:
            tm = datetime.now().date()
            addr = parseUrl(url)
            self.__cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (addr, tm))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def getUrl(self, url_id):

        try:
            self.__cur.execute("""SELECT id, name, created_at FROM urls
                                WHERE id = %s""", (url_id,))

            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False

            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getId(self, url):
        try:

            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД '+str(e))

        return False


    def getUnique(self):
        try:
            self.__cur.execute(f"""SELECT * FROM urls
                                ORDER BY created_at LIMIT 5""")
            res = self.__cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return res

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False
