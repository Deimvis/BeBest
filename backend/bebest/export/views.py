from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from posts.models import Post
from vacancies.models import VacancyArea, VacancyStats
from .forms import ExportPostsForm, ExportVacancyStatsForm
from .models import DatacampPost, DatacampVacancyStats, ExportLog


def index(request):
    def beautify(log_dict: dict) -> str:
        iso_dateteime = datetime.utcfromtimestamp(log_dict['timestamp']).isoformat()
        return f'{iso_dateteime} | {log_dict["destination_table_name"]} <— {log_dict["source_table_name"]}'

    logs = ExportLog.objects.order_by('-timestamp')
    beauty_logs = [beautify(model_to_dict(log)) for log in logs]
    return render(request, 'export/index.html', {'logs': beauty_logs})


@staff_member_required
@transaction.atomic
def export_posts(request):
    if request.method == 'POST':
        form = ExportPostsForm(request.POST)
        if form.is_valid():
            _export_posts()
            return HttpResponseRedirect(reverse('export:index'))
    else:
        form = ExportPostsForm()
    return render(request, 'export/export_posts.html', {'form': form})


@staff_member_required
@transaction.atomic
def export_vacancy_stats(request):
    if request.method == 'POST':
        form = ExportVacancyStatsForm(request.POST)
        if form.is_valid():
            _export_vacancy_stats()
            return HttpResponseRedirect(reverse('export:index'))
    else:
        form = ExportPostsForm()
    return render(request, 'export/export_vacancy_stats.html', {'form': form})


def _export_posts() -> dict:
    Post.objects.all().delete()
    for datacamp_post in DatacampPost.objects.all():
        post = Post(
            canonized_url = datacamp_post.canonized_url,
            source_name = datacamp_post.source_name,
            original_url = datacamp_post.original_url,
            title = datacamp_post.title,
            topics = datacamp_post.topics,
            rank = datacamp_post.rank,
            starting_text = datacamp_post.starting_text,
            publish_timestamp = datacamp_post.publish_timestamp,
            author_username = datacamp_post.author_username,
            views = datacamp_post.views,
        )
        post.save()
    timestamp = int(timezone.now().timestamp())  # UTC
    ExportLog(
        source_table_name = DatacampPost.objects.model._meta.db_table,
        destination_table_name = Post.objects.model._meta.db_table,
        timestamp = timestamp,
    ).save()
    return {
        'status': 'Done',
        'timestamp': timestamp,
    }


def _export_vacancy_stats() -> dict:
    VacancyStats.objects.all().delete()
    VacancyArea.objects.all().delete()
    area_ids_seen = set()
    for row in DatacampVacancyStats.join_area():
        vacancy_stats = VacancyStats(
            source_name=row['source_name'],
            area_id=row['area_id'],
            area_country_name=row['country_name'],
            area_city_name=row['city_name'],
            speciality=row['speciality'],
            tags=row['tags'],
            salary_currency=row['salary']['currency'],
            salary_from=row['salary']['from'],
            salary_to=row['salary']['to'],
        )
        vacancy_stats.save()
        if row['area_id'] not in area_ids_seen:
            area_ids_seen.add(row['area_id'])
            vacancy_area = VacancyArea(
                id=row['area_id'],
                country_name=row['country_name'],
                city_name=row['city_name'],
            )
            vacancy_area.save()
    timestamp = int(timezone.now().timestamp())  # UTC
    ExportLog(
        source_table_name = DatacampVacancyStats.objects.model._meta.db_table,
        destination_table_name = VacancyStats.objects.model._meta.db_table,
        timestamp = timestamp,
    ).save()
    return {
        'status': 'Done',
        'timestamp': timestamp,
    }

# transactional swap
# https://dba.stackexchange.com/a/100787
