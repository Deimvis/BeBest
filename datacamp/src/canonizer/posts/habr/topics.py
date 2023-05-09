from collections import defaultdict
from typing import List
from src.controller.posts.model import Topic
from src.crawler.posts.habr.models import Article


TOPIC2HUBS = {
    Topic.DEVELOPMENT: {
        'Программирование *',
        'Python *',
        'JavaScript *',
        'C *',
        'C# *',
        'C++ *',
        'Java *',
        'Go *',
        'Django *',
        'Flask *',
        'Алгоритмы *',
        'Распределённые системы *',
        'Промышленное программирование *',
    },
    Topic.BACKEND: {
        'Python *',
        'Java *',
        'Go *',
        'Django *',
        'Распределённые системы *',
        'API *',
    },
    Topic.FRONTEND: {
        'JavaScript *',
        'ReactJS *',
        'Node.JS *',
        'Angular *',
        'API *',
        'CSS *',
        'HTML *',
    },
    Topic.MACHINE_LEARNING: {
        'Машинное обучение *',
        'Искусственный интеллект ',
        'Natural Language Processing *',
        'TensorFlow *',
    },
}



def _build_HUB2TOPICS():
    hub2topics = defaultdict(set)
    for topic, hubs in TOPIC2HUBS.items():
        for hub in hubs:
            hub2topics[hub].add(topic)
    return hub2topics

HUB2TOPICS = _build_HUB2TOPICS()


def match_to_topics(article: Article) -> List[str]:
    topics = set()
    for hub in article.hubs:
        topics.update(HUB2TOPICS.get(hub, {}))
    return list(sorted(topics))
