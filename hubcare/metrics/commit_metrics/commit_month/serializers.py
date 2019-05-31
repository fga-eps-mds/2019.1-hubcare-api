from rest_framework import serializers
from commit_month.models import CommitMonth


class CommitMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitMonth
        fields = [
            'total_commits',
            'commits_week'
        ]
