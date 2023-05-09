from django.db import models


class Language(models.Model):
    ENGLISH = 'en'
    RUSSIAN = 'ru'
    ID_CHOICES = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian'),
    ]

    id = models.CharField(primary_key=True, max_length=3, choices=ID_CHOICES)
