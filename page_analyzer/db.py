import psycopg2
from datetime import datetime
from page_analyzer.validator import (parseUrl, normalizeNested,
                                     normalizeSimple, siteAnalize)


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
            print("Ошибка добавления адреса в БД "+str(e))
            return False
        return True

    def addCheck(self, id, status):
        page = self.getPageById(id)
        data = siteAnalize(page['name'])
        h1 = data['h1']
        title = data['title']
        description = data['description']
        try:
            tm = datetime.now()
            url_id = id
            status_code = status
            self.__cur.execute("""INSERT INTO url_checks
                                    (url_id, status_code, h1, title,
                                    description , created_at)
                                    VALUES (%s, %s, %s, %s, %s, %s)""",
                               (url_id, status_code, h1, title, description, tm))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления записи в БД "+str(e))
            return False
        return True

    def getCheckPage(self, url_id):
        try:
            self.__cur.execute(f"""SELECT *
                                  FROM url_checks
                                  WHERE url_id = {url_id}
                                  ORDER BY id
                                  DESC""")
            res = self.__cur.fetchall()
            if not res:
                print('Проверка не найдена')
                return False
            return normalizeNested(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getPageById(self, url_id):

        try:
            self.__cur.execute(f"""SELECT * FROM urls
                                WHERE id = {url_id} LIMIT 1""")

            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False

            return normalizeSimple(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))

        return False

    def getUrl(self, url):
        try:
            url = parseUrl(url)
            self.__cur.execute("""SELECT * FROM urls
                                WHERE name = %s""", (url,))
            res = self.__cur.fetchone()
            if not res:
                print('Cайт не найден')
                return False
            return normalizeSimple(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД '+str(e))

        return False

    def getUnique(self):
        try:
            self.__cur.execute("""SELECT * FROM urls ORDER BY created_at DESC LIMIT 5""")
            res = self.__cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return normalizeNested(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))
            return False

    def getAllChecks(self):
        try:
            self.__cur.execute("""SELECT * FROM url_checks ORDER BY id DESC LIMIT 5""")
            res = self.__cur.fetchall()
            if not res:
                print('Таблица пуста')
                return False
            return normalizeNested(res)

        except psycopg2.Error as e:
            print('Ошибка получения данных из БД: ' + str(e))
            return False
