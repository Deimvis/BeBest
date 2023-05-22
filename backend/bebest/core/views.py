import django.contrib.auth as auth
from django.contrib import messages
from django.shortcuts import render, redirect
from posts.models import Post

from .forms import SignupForm, LoginForm


def index(request):
    most_ranked_posts = Post.objects.order_by('-rank')[:10]
    return render(request, 'core/index.html', dict(posts=most_ranked_posts))


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        new_user = auth.authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        auth.login(request, new_user)
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return redirect('/')

    return render(request, 'core/signup.html', dict(form=form, query_string=request.META['QUERY_STRING']))


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        user = auth.authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('/')
        else:
            form.errors['password'] = 'Invalid username or password'
    return render(request, 'core/login.html', dict(form=form))


def logout(request):
    auth.logout(request)
    if request.method == 'GET' and 'next' in request.GET:
        return redirect(request.GET.get('next'))
    return redirect('/')
