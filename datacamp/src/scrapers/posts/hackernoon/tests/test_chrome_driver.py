import unittest
from src.scrapers.posts.hackernoon.chrome_driver import create_chrome_driver


class TestChromeDriver(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = create_chrome_driver(use_proxy=False)
        cls.proxy_driver = create_chrome_driver(use_proxy=True)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.proxy_driver.quit()

    def test_smoke(self):
        _ = self.driver

    def test_simple(self):
        self.driver.get('https://github.com/Deimvis')

    def test_simple_with_proxy(self):
        self.proxy_driver.get('https://github.com/Deimvis')
