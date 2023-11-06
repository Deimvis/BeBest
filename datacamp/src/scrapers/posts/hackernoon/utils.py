from typing import Dict
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

def update_url_params(url: str, params: Dict) -> str:
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)
