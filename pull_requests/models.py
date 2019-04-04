from django.db import models

class PullRequestTemplate(models.Model):
    
    url = models.CharField(max_length = 200)
    html_url = models.CharField(max_length = 200)
