from rest_framework import serializers
from license_metric.models import License


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = '__all__'
