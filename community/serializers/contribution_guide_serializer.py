from rest_framework import serializers
from community.models.contribution_guide_model import ContributionGuide


class ContributionGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContributionGuide
        fields = '__all__'
