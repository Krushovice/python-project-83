import math
import time
import psycopg2
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()



    def getUrls(self, url_id):
        try:
            self.__cur.execute(f"""SELECT * FROM urls
                                ORDER BY created_at
                                LIMIT 1""")

            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return res

        # except sqlite3.Error as e:
        #     print('Ошибка получения данных из БД '+str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"""SELECT * FROM users WHERE
                               email = '{email}' LIMIT 1""")

            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res

        except sqlite3.Error as e:
            print('Ошибка получения данных из БД '+str(e))

        return False

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"""SELECT COUNT() as 'count' FROM users
                               WHERE email LIKE '{email}'""")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с такой почтой уже существует!')
                return False

            tm = math.floor(time.time())
            self.__cur.execute("""INSERT INTO users VALUES
                                (NULL, ?, ?, ?, NULL, ?)""",
                               (name, email, hpsw, tm))
            self.__db.commit()

        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД '+str(e))
            return False

        return True

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"""SELECT COUNT() as 'count' FROM posts
                               WHERE url LIKE '{url}'""")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким url уже существует')
                return False
            base = url_for('static', filename='images')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>", text)

            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)',
                               (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"""SELECT title, text FROM posts
                               WHERE url LIKE '{alias}' LIMIT 1""")
            res = self.__cur.fetchone()
            if res:
                return res

        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return (False, False)
