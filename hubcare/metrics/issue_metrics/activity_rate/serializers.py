from rest_framework import serializers
from .models import ActivityRateIssue


class ActivityRateIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRateIssue
        fields = [
            'activity_rate',
            'activity_rate_15_days',
            'activity_rate_15_days_metric'
        ]
