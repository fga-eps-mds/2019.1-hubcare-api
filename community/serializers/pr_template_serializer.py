from rest_framework import serializers
from community.models.pr_template_model import Community

class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = '__all__'