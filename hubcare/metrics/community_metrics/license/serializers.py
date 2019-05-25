from rest_framework import serializers
from license.models import License


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = [
            'license'
        ]
