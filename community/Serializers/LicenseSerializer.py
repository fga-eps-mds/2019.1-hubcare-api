from rest_framework import serializers
from community.Models.LicenseModel import License

class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = '__all__'