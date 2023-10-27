import validators
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def validate(url):
    return True if validators.url(url) else False


def toValidString(url):
    h = urlparse(url)
    res = f'{h.scheme}://{h.hostname}'
    return res


def getStatus(url):
    try:
        r = requests.get(url)
        status = r.status_code
        return status

    except requests.exceptions.RequestException:
        print('Сайт недействителен')


def siteAnalize(url):
    try:
        response = requests.get(url)
        data = {'title': '',
                'h1': '',
                'description': ''
                }

        if response.status_code == 200:
            # Определение кодировки из заголовков HTTP, если указано
            content_type = response.headers.get('content-type')
            if content_type and 'charset' in content_type:
                encoding = content_type.split('charset=')[-1]
            else:
                encoding = 'utf-8'  # По умолчанию UTF-8

            # Декодирование текста с учетом кодировки
            decoded_text = response.content.decode(encoding, 'ignore')
            soup = BeautifulSoup(decoded_text, 'html.parser')
            title = soup.find('title')
            meta_description = soup.find('meta', attrs={'name': 'description'})
            h1 = soup.find('h1')
            data['title'] = title.text if title else ''
            if meta_description:
                data['description'] = meta_description.get('content')
            else:
                ''
            data['h1'] = h1.text if h1 else ''

        else:
            print(f'Ошибка при получении. Статус-код: {response.status_code}')

        return data
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при отправке запроса: {e}')


def normalizeNested(data):
    keys_for_urls = ['id', 'name', 'date']
    keys_for_checks = ['id', 'url_id', 'status_code', 'h1', 'title', 'description', 'date']

    def format_data(item):
        keys = keys_for_checks if len(item) == 7 else keys_for_urls
        item_dict = {key: value for key, value in zip(keys, item)}

        return item_dict

    result = [format_data(item) for item in data]
    return result


def normalizeSimple(data):
    keys_for_urls = ['id', 'name', 'date']
    keys_for_checks = ['id', 'url_id', 'status_code', 'h1', 'title', 'description', 'date']
    if len(data) > 3:
        keys = keys_for_checks
    else:
        keys = keys_for_urls
    result = {key: value for key, value in zip(keys, data)}

    return result


print(validate('http://wrong.com'))
