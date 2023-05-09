from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import Post

from django.forms.models import model_to_dict


def index(request):
    most_ranked_posts = Post.objects.order_by('-rank')[:10]
    return HttpResponse('Hello, world!' + '<br>' + '<br>'.join(map(lambda p: str(model_to_dict(p)), most_ranked_posts)))
    return render(request, 'posts/index.html', {'most_ranked_posts': most_ranked_posts})


def detail(request, post_id, beautify=True):
    post = get_object_or_404(Post, id=post_id)
    json_dumps_params={}
    if beautify:
        json_dumps_params={'indent': 2}
    return JsonResponse(model_to_dict(post), json_dumps_params=json_dumps_params)


def handling_404(request, exception):
    return HttpResponse('So sad, but it\'s a 404 :(')
