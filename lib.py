import requests
from contextlib import contextmanager
from bs4 import BeautifulSoup as _BeautifulSoup


def url_get(url, proxies=False, headers=None):

    if not proxies:
        proxies = {}
    with requests.Session() as session:
        return session.get(url, headers=headers, proxies=proxies).content


def soup(content='', headers=None):

    if content.startswith('http'):
        content = url_get(content, headers=headers)

    if content:
        _soup = _BeautifulSoup(content, 'lxml')
        # soup.find('title', attrs={'itemprop': "name"})
        return _soup
    return None


@contextmanager
def catch_exceptions(*exceptions, message=None):
    """
    manager for catch exceptions
    Application examples:

    >>> with catch_exceptions():
    ...     1/0
    ZeroDivisionError('division by zero',)

    >>> with catch_exceptions(KeyError, ZeroDivisionError):
    ...     1/0
    ZeroDivisionError('division by zero',)

    >>> with catch_exceptions(KeyError):
    ...     1/0
    ...
    Traceback (most recent call last):
          ...
    ZeroDivisionError: division by zero
    """
    if not exceptions:
        exceptions = (Exception,)
    try:
        yield
    except exceptions as e:
        try:
            if message is None:
                message = 'MANAGER CATCH '

            if message:
                logger.error(message + f'Exception: {repr(e)} \n traceback: {traceback.format_exc()}')
        except Exception as e:
            pass

    return True
