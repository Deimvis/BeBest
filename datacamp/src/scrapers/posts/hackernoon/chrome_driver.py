import contextlib
import itertools
import os
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver


@contextlib.contextmanager
def chrome_driver(use_proxy=False):
    driver = create_chrome_driver(use_proxy=use_proxy)
    try:
        yield driver
    finally:
        driver.quit()


def create_chrome_driver(use_proxy=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--pageLoadStrategy=normal')
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    seleniumwire_options = {}
    if use_proxy:
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{os.getenv("REQUESTS_HTTPS_PROXY")}',
                'https': f'https://{os.getenv("REQUESTS_HTTPS_PROXY")}',
            },
        }
        # _apply_proxy(chrome_options)

    return webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)


def _apply_proxy(chrome_options):
    username, password, host, port = itertools.chain.from_iterable(map(lambda s: s.split(':'), os.getenv('REQUESTS_HTTPS_PROXY').split('@')))

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
    );
    """ % (host, port, username, password)

    pluginfile = 'proxy_auth_plugin.zip'
    import zipfile
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)
