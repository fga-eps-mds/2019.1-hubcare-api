from rest_framework import serializers
from .models import ActivityRateIssue


class ActivityRateIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRateIssue
        fields = '__all__'
