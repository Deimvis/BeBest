from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.export_posts, name='posts'),
    path('vacancy_stats', views.export_vacancy_stats, name='vacancy_stats'),
]
