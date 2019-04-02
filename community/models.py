from django.db import models


class License(models.Model):

    key = models.CharField(max_length = 150)
    name =  models.CharField(max_length = 150)
    spdx_id = models.CharField(max_length = 150)
    url = models.CharField(max_length = 150)
    node_id = models.CharField(max_length = 150)

