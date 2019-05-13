from rest_framework import serializers
from hubcare_api.models import HubcareAPI


class HubcareAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = HubcareAPI
        fields = '__all__'
