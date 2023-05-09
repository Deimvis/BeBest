from django.shortcuts import render, redirect

from posts.models import Post

from .forms import SignupForm


def index(request):
    most_ranked_posts = Post.objects.order_by('-rank')[:10]
    return render(request, 'core/index.html', dict(posts=most_ranked_posts))


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', dict(form=form))
