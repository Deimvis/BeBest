from urllib.parse import urlparse, urlunparse


def canonize_url(url) -> str:
    parsed_original = urlparse(url)
    parsed_canonized = parsed_original._replace(query='')
    return urlunparse(parsed_canonized)
