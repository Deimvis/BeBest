import random
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post
from .view_models import PostView
from urllib.parse import urlparse, urlunparse

from django.forms.models import model_to_dict


def index(request):
    speciality = request.GET['speciality']
    if speciality not in ('frontend', 'backend', 'machine_learning'):
        return redirect(reverse('posts:index') + '?speciality=frontend')

    db_speciality = f'development/{speciality}'
    posts_sample = _extract_posts_sample(db_speciality)
    view_posts_sample = [PostView.from_post(post) for post in posts_sample]
    beautiful_speciality = _beautify_speciality(db_speciality)
    refresh_url = _build_refresh_url(request)
    ctx = {
        'speciality': speciality,
        'beautiful_speciality': beautiful_speciality,
        'posts': view_posts_sample,
        'refresh_url': refresh_url,
    }
    return render(request, 'posts/index.html', ctx)


def detail(request, post_id, beautify=True):
    post = get_object_or_404(Post, id=post_id)
    json_dumps_params={}
    if beautify:
        json_dumps_params={'indent': 2}
    return JsonResponse(model_to_dict(post), json_dumps_params=json_dumps_params)


def handling_404(request, exception):
    return HttpResponse('So sad, but it\'s a 404 :(')


def _extract_posts_sample(speciality: str):
    most_ranked_posts = list(Post.objects.filter(topics__contains=[speciality]).order_by('-rank')[:100])
    random.shuffle(most_ranked_posts)
    posts_sample = most_ranked_posts[:12]
    posts_sample.sort(key=lambda post: -post.rank)
    return posts_sample

def _beautify_speciality(speciality: str):
    match speciality:
        case 'development/frontend':
            return 'Frontend'
        case 'development/backend':
            return 'Backend'
        case 'development/machine_learning':
            return 'Machine Learning'
        case _:
            raise RuntimeError(f'Got unsupported speciality: {speciality}')

def _build_refresh_url(request) -> str:
    refresh_params = request.GET.dict()
    refresh_params.pop('box_animation', None)
    refresh_params_str = '&'.join([f'{k}={v}' for k, v in refresh_params.items()])
    return reverse('posts:index') + '?' + refresh_params_str
