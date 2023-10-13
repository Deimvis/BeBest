import unittest
from src.scrapers.plan_base import ScrapePlanBase


class TestScrapePlanBase(unittest.TestCase):

    def test_smoke(self):
        _ = type('MyScrapePlan', (ScrapePlanBase,), {})
