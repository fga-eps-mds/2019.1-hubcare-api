from rest_framework import serializers
from .models import ActivityRateIssue


class ActivityRateIssueSerializers(serializers.ModelSerializer):

    class Meta:
        model = ActivityRateIssue
        fields = '__all__'
