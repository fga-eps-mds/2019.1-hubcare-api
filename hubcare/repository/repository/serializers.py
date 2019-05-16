from rest_framework import serializers
from repository.models import Repository
from datetime import datetime, timezone


class RepositorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Repository
        fields = [
            'owner',
            'repo',
            'date_time'
        ]
