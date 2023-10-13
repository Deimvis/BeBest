import math
from src.scrapers.posts.habr.models import Article


def calculate_rank(article: Article, views: int) -> int:
    return 5 + int(math.log(views, 10))
