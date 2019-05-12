from rest_framework.views import APIView
from rest_framework.response import Response
from release_note.models import ReleaseNoteCheck
from release_note.serializers import ReleaseNoteCheckSerializers
from datetime import datetime, timedelta
import requests
import json
import os
from community_metrics.functions import serialized_object
from community_metrics.constants import URL_API, HTTP_OK, NINETY_DAYS


class ReleaseNoteCheckView(APIView):

    def get(self, request, owner, repo):

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        releasenotecheck = ReleaseNoteCheck.objects.all().filter(
            owner=owner,
            repo=repo
        )
        releasenotecheck_serialized = serialized_object(
            ReleaseNoteCheckSerializers,
            releasenotecheck
            )
        github_request = requests.get(
            URL_API + owner + '/' + repo + '/releases',
            auth=(username, token)
        )
        github_data = github_request.json()
        present = datetime.today()
        days = timedelta(days=NINETY_DAYS)
        releaseDays = present - days
        releaseLastNinetyDays = []
        response = False
        if(github_data != []):
            releaseDate = datetime.strptime(
                github_data[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            if(releaseDate > releaseDays):
                response = True
        response = {
            'response': response
        }

        response = json.loads(json.dumps(response))
        return Response(response)
