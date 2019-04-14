from rest_framework import serializers
from commits.models import CommitWeek


class CommitWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitWeek
        fields = '__all__'
