import django.contrib.postgres.fields as postgres_fields
from django.db import connection, models
from typing import Dict


class ExportLog(models.Model):
    source_table_name = models.CharField(max_length=256)
    destination_table_name = models.CharField(max_length=256)
    timestamp =  models.BigIntegerField()


class DatacampArea(models.Model):
    id = models.BigIntegerField(primary_key=True)
    country_name = models.CharField(max_length=256)
    city_name = models.CharField(max_length=256)
    hh_id = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datacamp_area'


class DatacampPost(models.Model):
    insert_timestamp = models.BigIntegerField(blank=True, null=True)
    resource_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    canonized_url = models.CharField(max_length=2048, primary_key=True)
    original_url = models.CharField(max_length=2048)
    title = models.CharField(max_length=256)
    topics = postgres_fields.ArrayField(models.CharField(max_length=256))
    rank = models.BigIntegerField()
    starting_text = models.TextField()
    publish_timestamp = models.BigIntegerField()
    author_username = models.CharField(max_length=128, blank=True, null=True)
    views = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datacamp_post'


class DatacampVacancyStats(models.Model):
    source_name = models.CharField(max_length=128)
    area_id = models.ForeignKey(DatacampArea, on_delete=models.DO_NOTHING, db_constraint=False)
    speciality = models.CharField(max_length=256)
    tags = postgres_fields.ArrayField(models.CharField(max_length=256))
    salary = models.JSONField()

    class Meta:
        managed = False
        db_table = 'datacamp_vacancy_stats'

    @staticmethod
    def join_area() -> Dict:
        query = """
            SELECT
                vacancy_stats.*,
                area.*
            FROM {vacancy_stats} as vacancy_stats
            JOIN {area} as area
                ON (vacancy_stats.area_id = area.id)
        """
        query = query.format(vacancy_stats=DatacampVacancyStats._meta.db_table, area=DatacampArea._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(query)
            col_names = [col[0] for col in cursor.description]
            result = cursor.fetchall()
            dict_result = [dict(zip(col_names, row)) for row in result]
            return dict_result
