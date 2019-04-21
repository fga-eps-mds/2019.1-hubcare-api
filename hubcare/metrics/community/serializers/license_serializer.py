from rest_framework import serializers
from community.models.license_model import License


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = '__all__'
