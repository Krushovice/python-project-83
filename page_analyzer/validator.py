import validators


def validate(url):
    return True if validators.url(url) else False
