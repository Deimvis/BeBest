import functools
import re
from bs4 import BeautifulSoup
from typing import Any, Dict


class ParserBaserMeta(type):
    """
    This metaclass for each 'parse_X' method
    creates correspoinding 'try_parse_X' method
    which wraps first in try-except block
    and in case of success puts result in dictionary.
    In order to get dictionary with results
    there is `GET_PARSING_RESULTS(self)` method.
    In order to run all `try_parse` methods at once
    there is `TRY_PARSE_EVERYTHING` method.
    """

    def __new__(cls, name, bases, classdict):
        assert 'TRY_PARSE_EVERYTHING' not in classdict, 'Do not create `TRY_PARSE_EVERYTHING` method, this name is reserved by ParserMeta'
        assert 'GET_PARSING_RESULTS' not in classdict, 'Do not create `GET_PARSING_RESULTS` method, this name is reserved by ParserMeta'

        parsing_results = {}
        def _try_parse(field_name: str):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    nonlocal parsing_results
                    try:
                        parsing_results[field_name] = func(*args, **kwargs)
                    except:
                        pass
                return wrapper
            return decorator

        try_parse_methods = {}
        for attr_name in classdict.keys():
            match_result = re.fullmatch(r'parse_(?P<field_name>.*)', attr_name)
            if match_result is not None:
                field_name = match_result.group('field_name')
                method = classdict[attr_name]
                try_parse_methods[f'try_parse_{field_name}'] = _try_parse(field_name)(method)

        def _TRY_PARSE_EVERYTHING(self):
            nonlocal try_parse_methods
            for method in try_parse_methods.values():
                method(self)

        def _GET_PARSING_RESULTS(self):
            nonlocal parsing_results
            return parsing_results

        new_methods = try_parse_methods | {'TRY_PARSE_EVERYTHING': _TRY_PARSE_EVERYTHING, 'GET_PARSING_RESULTS': _GET_PARSING_RESULTS}
        return type(name, bases, classdict | new_methods)


class ParserBase():
    def __init__(self, soup: BeautifulSoup | None = None):
        self.soup = soup

    def TRY_PARSE_EVERYTHING(self) -> None:
        raise AttributeError('method should be overriden by metaclass')

    def GET_PARSING_RESULTS(self) -> Dict[str, Any]:
        raise AttributeError('method should be overriden by metaclass')
