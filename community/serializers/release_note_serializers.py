from rest_framework import serializers
from community.models.release_note_models import ReleaseNoteCheck


class ReleaseNoteCheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReleaseNoteCheck
        fields = '__all__'
