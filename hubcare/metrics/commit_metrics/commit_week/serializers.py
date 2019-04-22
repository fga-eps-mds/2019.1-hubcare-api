from rest_framework import serializers
from commit_week.models import CommitWeek


class CommitWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitWeek
        fields = '__all__'
