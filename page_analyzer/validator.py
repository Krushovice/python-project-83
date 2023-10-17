import validators
from urllib.parse import urlparse
from datetime import datetime


def validate(url):
    return True if validators.url(url) else False



def parseUrl(url):
    h = urlparse(url)
    res = f'{h.scheme}://{h.hostname}'
    return res
