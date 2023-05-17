import functools
import re
from bs4 import BeautifulSoup


class ParserBaserMeta(type):
    """
    This metaclass for each 'parse_X' method
    creates correspoinding 'try_parse_X' method
    which wraps first in try-except block
    and in case of success puts result in dictionary.
    In order to get dictionary with results
    there is `get_parsing_results(self)` method.
    In order to run all `try_parse` methods at once
    there is `try_parse_EVERYTHING` method.
    """

    def __new__(cls, name, bases, classdict):
        assert 'try_parse_EVERYTHING' not in classdict, 'Do not create `try_parse_EVERYTHING` method, this name is reserved by ParserMeta'
        assert 'get_parsing_results' not in classdict, 'Do not create `get_parsing_results` method, this name is reserved by ParserMeta'

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

        def _try_parse_EVERYTHING(self):
            nonlocal try_parse_methods
            for method in try_parse_methods.values():
                method(self)

        def _get_parsing_results(self):
            nonlocal parsing_results
            return parsing_results

        new_methods = try_parse_methods | {'try_parse_EVERYTHING': _try_parse_EVERYTHING, 'get_parsing_results': _get_parsing_results}
        return type(name, bases, classdict | new_methods)


class ParserBase():
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
