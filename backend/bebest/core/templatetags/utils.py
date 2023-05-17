from django import template
from urllib.parse import quote

register = template.Library()


@register.filter('startswith')
def startswith(text, prefix):
    if isinstance(text, str):
        return text.startswith(prefix)
    return False


@register.filter('urlencode')
def urlencode(url):
    return quote(url)
