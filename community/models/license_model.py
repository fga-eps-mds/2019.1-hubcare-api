from django.db import models


class License(models.Model):

    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    have_license = models.BooleanField(default=False)
    date = models.DateField(default=None)
