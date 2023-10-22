import validators
import re
from urllib.parse import urlparse
from datetime import datetime


def validate(url):
    return True if validators.url(url) else False



def parseUrl(url):
    h = urlparse(url)
    res = f'{h.scheme}://{h.hostname}'
    return res


def normalize_str(data):
    result = {}

    for item in data:
        match = re.search(r'\((\d+),([^,]+),(\d{4}-\d{2}-\d{2})\)', item)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                id, value, date = groups
                result.update({'id': id, 'name': value, 'date': date})
            elif len(groups) == 2:
                id, date = groups
                result.update({'id': id, 'date': date})
    return result


def normalize(data):
    keys_for_urls = ['id', 'name', 'date']
    keys_for_checks = ['id', 'url_id', 'status_code', 'h1', 'title', 'discription', 'date']
    if len(data) > 3:
        keys = keys_for_checks
    else:
        keys = keys_for_urls
    result = {key: value for key, value in zip(keys, data)}

    return result
