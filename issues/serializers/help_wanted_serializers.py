from rest_framework import serializers
from issues.models.help_wanted_models import HelpWanted

class HelpWantedSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpWanted
        fields = '__all__'