import django.contrib.postgres.fields as postgres_fields
from django.db import connection, models
from typing import Dict, List, Self


class VacancyStats(models.Model):
    class SourceName(models.TextChoices):
        HH_API = 'hh_api'

    class Speciality(models.TextChoices):
        FRONTEND = 'development/frontend'
        BACKEND = 'development/backend'
        MACHINE_LEARNING = 'development/machine_learning'

    class SalaryCurrency(models.TextChoices):
        RUB = 'RUR'
        USD = 'USD'

    source_name =       models.CharField(max_length=128, choices=SourceName.choices)
    area_id =           models.BigIntegerField(db_index=True)
    area_country_name = models.CharField(max_length=256)
    area_city_name =    models.CharField(max_length=256)
    speciality =        models.CharField(max_length=256, choices=Speciality.choices)
    tags =              postgres_fields.ArrayField(models.CharField(max_length=256))
    salary_currency =   models.CharField(max_length=64, choices=SalaryCurrency.choices)
    salary_from =       models.BigIntegerField(null=True)
    salary_to =         models.BigIntegerField(null=True)

    def __str__(self) -> str:
        return f'Vacancy, salary: {self.salary_from} - {self.salary_to})'

    @staticmethod
    def tags_by_speciality(speciality: str) -> List[str]:
        assert speciality in VacancyStats.Speciality.choices()
        VacancyStats.objects.filter(speciality=speciality).distinct('tags')

    @staticmethod
    def calc_target_stats(area_id: int, speciality: str) -> Dict:
        query = """
            SELECT
                ROUND(AVG(salary_from), 2) AS avg_from,
                ROUND(AVG(salary_to), 2) AS avg_to,
                ROUND(AVG((salary_from + COALESCE(salary_to, salary_from)) / 2), 2) AS avg_middle
            FROM {vacancy_stats}
            WHERE salary_from IS NOT NULL
                AND salary_currency = 'RUR'
                AND area_id = %s AND speciality = %s
        """
        query = query.format(vacancy_stats=VacancyStats._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(query, [area_id, speciality])
            col_names = [col[0] for col in cursor.description]
            result = cursor.fetchall()
            dict_result = [dict(zip(col_names, row)) for row in result]
            return dict_result[0]

    @staticmethod
    def example() -> Self:
        return VacancyStats(
            source_name='hh_api',
            area_id=1,
            area_country_name='Russia',
            area_city_name='Moscow',
            speciality='development/backend',
            tags=['Python'],
            salary_currency='RUB',
            salary_from=150000,
            salary_to=250000,
        )


class VacancyArea(models.Model):
    id =           models.BigIntegerField(primary_key=True)
    country_name = models.CharField(max_length=256)
    city_name =    models.CharField(max_length=256)

    @property
    def location(self) -> str:
        return f'{self.country_name}/{self.city_name}'

    @staticmethod
    def distinct_locations() -> List[str]:
        locs = set()
        for va in VacancyArea.objects.all():
            locs.add(va.location)
        return list(locs)
