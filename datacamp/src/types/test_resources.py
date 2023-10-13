import unittest
from src.types import ResourceName


class TestResourceName(unittest.TestCase):

    def test_smoke(self):
        _ = ResourceName.POST

    def test_valid_type(self):
        self.assertIsInstance(ResourceName.POST, str)
        self.assertIsInstance(ResourceName.VACANCY, str)
