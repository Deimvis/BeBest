from django.urls import path

from . import views

app_name = 'vacancies'
urlpatterns = [
    path('', views.index, name='index'),
]
