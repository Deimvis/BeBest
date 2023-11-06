from collections import defaultdict
from typing import List
from src.types.specialities import Speciality
from src.scrapers.posts.hackernoon.models import Article


TOPIC2TAGS = {
    Speciality.DEVELOPMENT.BACKEND: {
        'backend',
        'python',
        'python3',
        'python-programming',
        'golang',
        'go',
        'java',
        'nodejs',
        'rust',
        'php',
        'ruby',
        'ruby-on-rails',
        'sql',
        'aws',
        'cloud',
        'cloud-computing',
        'devops',
        'api',
        'rest-api',
        'docker',
        'serverless',
        'big-data',
        'kubernetes',
        'database',
        'software-architecture',
        'microservices',
        'linux',
        'cyber-security',
        'graphql',
        'distributed-systems',
        'django',
        'spring-boot',
        'spring-mvc',
        'java-spring-boot',
        'database',
        'postgres',
        'mongodb',
        'clickhouse',
    },
    Speciality.DEVELOPMENT.FRONTEND: {
        'front-end-development',
        'frontend',
        'html',
        'react',
        'reactjs',
        'react-native',
        'vuejs',
        'typescript',
        'angular',
        'docker',
    },
    Speciality.DEVELOPMENT.MACHINE_LEARNING: {
        'machine-learning',
        'ml',
        'data-science',
        'deep-learning',
        'data-analysis',
        'data-analytics',
        'nlp',
        'python',
        'python3',
        'python-programming',
        'sql',
        'docker',
    },
}



def _build_TAG2TOPICS():
    hub2topics = defaultdict(set)
    for topic, hubs in TOPIC2TAGS.items():
        for hub in hubs:
            hub2topics[hub].add(topic)
    return hub2topics

TAG2TOPICS = _build_TAG2TOPICS()


def match_to_topics(article: Article) -> List[str]:
    topics = set()
    for tag in article.tags:
        topics.update(TAG2TOPICS.get(tag, {}))
    return list(sorted(topics))
