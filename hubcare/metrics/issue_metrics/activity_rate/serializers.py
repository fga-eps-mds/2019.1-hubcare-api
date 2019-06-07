from rest_framework import serializers
from .models import ActivityRateIssue


class ActivityRateIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRateIssue
        fields = [
            'activity_rate',
            'activity_max_rate',
            'active_issues',
            'dead_issues'
        ]
