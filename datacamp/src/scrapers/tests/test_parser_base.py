import requests
import unittest
from bs4 import BeautifulSoup
from src.scrapers.parser_base import ParserBase, ParserBaserMeta


class TestParserBaserMeta(unittest.TestCase):
    class MyParser(metaclass=ParserBaserMeta):
        def parse_xyz(self):
            return 'xyz123'

    def test_smoke(self):
        _ = self.MyParser()

    def test_TRY_PARSE_EVERYTHING(self):
        self.MyParser().TRY_PARSE_EVERYTHING()

    def test_GET_PARSING_RESULTS(self):
        parser = self.MyParser()
        parser.TRY_PARSE_EVERYTHING()
        result = parser.GET_PARSING_RESULTS()
        self.assertEqual(result, {'xyz': 'xyz123'})


class TestParserBase(unittest.TestCase):
    class MyParser(ParserBase, metaclass=ParserBaserMeta):
        def parse_xyz(self):
            return 'xyz123'

    @classmethod
    def setUpClass(cls):
        cls.soup = BeautifulSoup(requests.get('https://github.com/').text, 'html.parser')

    def test_smoke(self):
        _ = self.MyParser(soup=self.soup)
