from django.db import models

class PullRequestTemplate(models.Model):

    pulls_url = models.CharField(max_length = 150)
