from django.db import models

class Community(models.Model):

    owner = models.CharField(max_length = 200)
    repo = models.CharField(max_length = 200)
    pull_request_template = models.BooleanField(default=False)
    date = models.DateField(default=None)
