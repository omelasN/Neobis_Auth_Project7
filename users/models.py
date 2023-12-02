from django.db import models


class Registration(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=20)
