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


def read_file(filename, TYPE=True, errors='ignore', **kwargs):
    """
    read file with kwargs:
    Defult TYPE = extpath of file

    TYPE variants:
        pkl: pickle.load(f)
        yaml: yaml.load(f)
        json: json.load(f)
        None or another: f.read()

    additional args:
    mode = 'r' - mode kwarg of open func
        byte mode auto set encoding=None
    encoding = 'utf-8' - encoding kwarg of open func.

    """

    mode = kwargs.get('mode', 'r')
    encoding = kwargs.get('encoding', 'utf-8') if 'b' not in mode else None

    if TYPE and isinstance(TYPE, bool):
        TYPE = os.path.splitext(filename)[-1][1:]
    try:
        if TYPE == 'pkl':
            with open(filename, 'rb') as f:
                return pickle.load(f)

        with open(filename, mode=mode, encoding=encoding) as f:
            if TYPE == 'yaml':
                return yaml.safe_load(f)
            elif TYPE == "json":
                return json.loads(f.read())
            # elif TYPE == 'csv':
            #     return list(csv.reader(f, **kwargs))
            else:
                return f.read()

    except Exception as e:
        logger.error(traceback.format_exc())
        if errors != 'ignore':
            raise e


def write_file(filename, input, mode=None):
    try:
        if not mode:
            with open(filename, 'w') as f:
                f.write(input)

        elif mode == 'wb' or isinstance(input, bytes):
            with open(filename, 'wb') as f:
                f.write(input)

        elif mode == 'pkl':
            with open(filename, 'wb') as f:
                pickle.dump(input, f)

        else:
            with open(filename, 'w') as f:
                if mode == 'json':
                    f.write(jdumps(input))
                elif mode == 'yaml':
                    f.write(ydumps(input))
                else:
                    f.write(input)
        return True
    except Exception as e:
        return str(e)



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
