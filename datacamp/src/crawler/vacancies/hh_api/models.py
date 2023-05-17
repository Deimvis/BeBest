from typing import Dict, List
from . import api_models



class Vacancy(api_models.Vacancy):
    speciality: str
    tags: List[Dict]

    @staticmethod
    def from_api_model(vacancy: api_models.Vacancy, speciality: str, tags: List[Dict]) -> 'Vacancy':
        return Vacancy(
            speciality=speciality,
            tags=tags,
            **vacancy.dict(),
        )
