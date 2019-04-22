from rest_framework import serializers
from help_wanted.models import HelpWanted


class HelpWantedSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpWanted
        fields = '__all__'
