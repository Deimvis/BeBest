from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'The Boss',
        'class': 'w-full py-2 px-2 rounded-xl',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'elon_musk@mars.com',
        'class': 'w-full py-2 px-2 rounded-xl',
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-2 px-2 rounded-xl',
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-2 px-2 rounded-xl',
    }))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'The Boss',
        'class': 'w-full py-2 px-2 rounded-xl',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-2 px-2 rounded-xl',
    }))