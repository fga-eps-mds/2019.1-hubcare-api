from rest_framework import serializers
from contribution_guide_metric.models import ContributionGuide


class ContributionGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContributionGuide
        fields = '__all__'
