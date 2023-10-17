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
    # def getUrl(self, url_id):
    #     try:
    #         self.__cur.execute(f"""SELECT * FROM urls
    #                             WHERE id = (url_id)""")

    #         res = self.__cur.fetchone()
    #         if not res:
    #             print('Cайт не найден')
    #             return False
    #         return res

    #     except psycopg2.Error as e:
    #         print('Ошибка получения данных из БД '+str(e))

        # return False



    # def getUrlChecks(self):
    #     try:
    #         self.__cur.execute(f"""SELECT title, text FROM posts
    #                            WHERE url LIKE '{alias}' LIMIT 1""")
    #         res = self.__cur.fetchone()
    #         if res:
    #             return res

    #     except psycopg2.Error as e:
    #         print("Ошибка получения статьи из БД "+str(e))

        # return (False, False)
