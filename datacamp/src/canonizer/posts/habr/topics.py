from collections import defaultdict
from typing import List
from src.types.specialities import Speciality
from src.crawler.posts.habr.models import Article


TOPIC2HUBS = {
    Speciality.DEVELOPMENT.BACKEND: {
        'Python *',
        'C *',
        'C# *',
        'C++ *',
        'Java *',
        'Go *',
        'API *',
        'Django *',
        'Flask *',
        'Алгоритмы *',
        'Распределённые системы *',
        'Распределённые системы *',
        'Промышленное программирование *',
    },
    Speciality.DEVELOPMENT.FRONTEND: {
        'JavaScript *',
        'ReactJS *',
        'Node.JS *',
        'Angular *',
        'API *',
        'CSS *',
        'HTML *',
    },
    Speciality.DEVELOPMENT.MACHINE_LEARNING: {
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
