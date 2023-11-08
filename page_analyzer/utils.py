import validators
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def is_valid(url):
    return True if validators.url(url) else False


def to_valid_string(url):
    h = urlparse(url)
    res = f'{h.scheme}://{h.hostname}'
    return res


def get_status(url):
    try:
        r = requests.get(url)

    except requests.exceptions.RequestException:
        logging.error('Сайт недействителен')

    status = r.status_code
    return status


def site_analize(url):
    data = {'title': '',
            'h1': '',
            'description': ''
            }
    try:
        response = requests.get(url)

    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при отправке запроса: {e}')

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
            data['description'] = ''
            data['h1'] = h1.text if h1 else ''

    else:
        logging.error(f'Ошибка при получении. Статус-код: {response.status_code}')

    return data


def normalize_simple(data):
    keys_for_urls = ['id', 'name', 'date']
    keys_for_checks = ['id', 'url_id', 'status_code', 'h1', 'title', 'description', 'date']
    if len(data) > 3:
        keys = keys_for_checks
    else:
        keys = keys_for_urls
    result = {key: value for key, value in zip(keys, data)}

    return result
