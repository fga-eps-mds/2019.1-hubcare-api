from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.release_note_models \
    import ReleaseNoteCheck
from community.serializers.release_note_serializers \
    import ReleaseNoteCheckSerializers
from datetime import datetime, timedelta
import requests


class ReleaseNoteCheckView(APIView):

    def get(self, request, owner, repo):
        releasenotecheck = ReleaseNoteCheck.objects.all().filter(
            owner=owner,
            repo=repo
        )
        releasenotecheck_serialized = ReleaseNoteCheckSerializers(
            releasenotecheck,
            many=True
        )
        github_request = requests.get(
            'https://api.github.com/repos/' + owner + '/' + repo + '/releases'
        )
        github_data = github_request.json()
        present = datetime.today()
        days = timedelta(days=90)
        releaseDays = present - days
        releaseLastNinetyDays = []

        if(github_data != []):
            releaseDate = datetime.strptime(github_data[0]['created_at'],"%Y-%m-%dT%H:%M:%SZ")
            if(releaseDate > releaseDays):
                return Response(True)
            else:
                return Response(False)
        else:
            return Response(False)

        