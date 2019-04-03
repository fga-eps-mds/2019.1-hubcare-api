from rest_framework import serializers
from .models import PullRequestTemplate

class PullRequestTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PullRequestTemplate
        fields = '__all__'