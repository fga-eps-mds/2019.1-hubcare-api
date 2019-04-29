from rest_framework import serializers
from .models import PullRequestQuality


class PullRequestQualitySerializers(serializers.ModelSerializer):

    class Meta:
        model = PullRequestQuality
        fields = '__all__'
