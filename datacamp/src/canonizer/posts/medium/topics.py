import logging
from collections import defaultdict
from typing import List
from src.types.specialities import Speciality
from src.scrapers.posts.medium.models import Article


TOPIC2TAGS = {
    Speciality.DEVELOPMENT.BACKEND: {
        'Backend',
        'Backend Development',
        'Software Engineering',
        'Software Development',
        'Distributed Systems',
        'Software Architecture',
        'Data Engineering',
        'Data Pipeline',
        'Bigquery',
        'Data',
    },
    Speciality.DEVELOPMENT.FRONTEND: {
        'Frontend',
        'Typescript',
        'Angular',
        'JavaScript',
    },
    Speciality.DEVELOPMENT.MACHINE_LEARNING: {
        'Data Science',
        'Machine Learning',

    },
}



def _build_TAG2TOPICS():
    tag2topics = defaultdict(set)
    for topic, tags in TOPIC2TAGS.items():
        for tag in tags:
            tag2topics[tag].add(topic)
    return tag2topics

TAG2TOPICS = _build_TAG2TOPICS()


def match_to_topics(article: Article) -> List[str]:
    topics = set()
    for tag in article.tags:
        topics.update(TAG2TOPICS.get(tag, set()))
    if len(article.tags) > 0 and len(topics) == 0:
        logging.info(f'No topics found for non-empty article tag list: {article.tags}')
    return list(sorted(topics))
