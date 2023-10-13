import unittest
from src.types.sources import SourceName


class TestSourceName(unittest.TestCase):

    def test_smoke(self):
        _ = SourceName.HABR

    def test_valid_type(self):
        self.assertIsInstance(SourceName.HABR, str)
        self.assertIsInstance(SourceName.MEDIUM, str)
        self.assertIsInstance(SourceName.DCM, str)
        self.assertIsInstance(SourceName.HH_API, str)
