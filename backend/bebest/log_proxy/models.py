from django.db import models


class UserLog(models.Model):
    class Action(models.TextChoices):
        GO_TO = 'go_to'

    timestamp = models.BigIntegerField()
    username = models.CharField(max_length=150, null=True)
    action = models.CharField(max_length=32, choices=Action.choices)
    action_value = models.CharField(max_length=1024, null=True)
