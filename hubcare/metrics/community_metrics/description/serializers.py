from rest_framework import serializers
from description.models import Description


class DescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Description
        fields = '__all__'
