import re
from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from typing import Dict

from .models import VacancyStats, VacancyArea
from .forms import VacancyStatsForm


def index(request):
    is_show_stats = request.method == 'GET' and all(param in request.GET for param in ['speciality', 'location'])
    is_initial = request.method == 'GET' and not is_show_stats
    is_submit_filters = request.method == 'POST'
    ctx = {}
    if is_initial:
        form = VacancyStatsForm()
    elif is_submit_filters:
        form = VacancyStatsForm(request.POST)
        if form.is_valid():
            return redirect(reverse('vacancies:index') + f'?speciality={form["speciality"].value()}&location={form["location"].value()}')
    if is_show_stats:
        location = request.GET['location']
        speciality = request.GET['speciality']
        form = VacancyStatsForm(initial={'speciality': speciality, 'location': location})
        area_id = _location2area_id(location)
        stats = VacancyStats.calc_target_stats(area_id, speciality)
        ctx['stats'] = _beautify_stats(stats)
    ctx['form'] = form
    return render(request, 'vacancies/index.html', ctx)


def _location2area_id(location: str) -> int:
    country_name, city_name = location.split('/')
    area = VacancyArea.objects.get(country_name=country_name, city_name=city_name)
    return area.id


def _beautify_stats(stats: Dict) -> Dict:
    is_float = lambda x: re.match(r'^-?\d+(?:\.\d+)$', x) is not None
    beauty_stats = {}
    for k, v in stats.items():
        if isinstance(v, str):
            if is_float(v):
                v = float(v)
            elif v.isdigit():
                v = int(v)
        if isinstance(v, int | float | Decimal):
            v = _make_salary_number(v)
            print('salary number:', v)
        beauty_stats[k] = v
    return beauty_stats


def _make_salary_number(x: int | float | Decimal) -> str:
    print('original number:', x)
    beauty_number = _beautify_number(int(x))
    print('beauty number:', beauty_number)
    int_beauty_number = beauty_number[:-3]
    if len(int_beauty_number) <= 3:
        return int_beauty_number
    return int_beauty_number[:-3] + '000'


def _beautify_number(x: int | float | Decimal) -> str:
    if isinstance(x, float | Decimal):
        suffix = '.' + str(x).split('.')[1]
    elif isinstance(x, int):
        suffix = '.00'
    x = int(x)
    reversed_number_blocks = []
    while x > 0:
        reversed_number_blocks.append(str(x % 1000).zfill(3))
        x //= 1000
    return '`'.join(reversed_number_blocks[::-1]) + suffix
