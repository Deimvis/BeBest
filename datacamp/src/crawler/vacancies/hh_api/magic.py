from src.types.specialities import Speciality

# MAGIC
MOSCOW_AREA_ID = '1'
ST_PETERSBURG_AREA_ID = '2'
CRAWL_AREAS = [MOSCOW_AREA_ID, ST_PETERSBURG_AREA_ID]
CRAWL_REQUESTS = [
    {
        'search_text': 'backend developer',
        'speciality': Speciality.DEVELOPMENT.BACKEND,
        'tags': []
    },
    {
        'search_text': 'бэкенд разработчик',
        'speciality': Speciality.DEVELOPMENT.BACKEND,
        'tags': []
    },
    {
        'search_text': 'frontend developer',
        'speciality': Speciality.DEVELOPMENT.FRONTEND,
        'tags': []
    },
    {
        'search_text': 'фронтенд разработчик',
        'speciality': Speciality.DEVELOPMENT.FRONTEND,
        'tags': []
    },
    {
        'search_text': 'machine learning developer',
        'speciality': Speciality.DEVELOPMENT.MACHINE_LEARNING,
        'tags': []
    },
    {
        'search_text': 'разработчик машинного обучения',
        'speciality': Speciality.DEVELOPMENT.MACHINE_LEARNING,
        'tags': []
    },
    {
        'search_text': 'data scientist',
        'speciality': Speciality.DEVELOPMENT.MACHINE_LEARNING,
        'tags': []
    },
]

