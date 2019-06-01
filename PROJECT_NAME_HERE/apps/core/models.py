from django.db import models


class Options(models.Model):

    key = models.CharField(max_length = 250, unique=True)
    value = models.TextField()
    label = models.CharField(max_length = 500)