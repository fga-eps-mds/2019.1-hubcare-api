from rest_framework import serializers
from .models import PullRequestQuality


class PullRequestQualitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PullRequestQuality
        fields = [
            'acceptance_rate'
        ]
