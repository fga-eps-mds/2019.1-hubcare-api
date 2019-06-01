from rest_framework import serializers
from .models import PullRequestQuality
import json


class PullRequestQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PullRequestQuality
        fields = [
            'acceptance_rate',
            'categories'
        ]
