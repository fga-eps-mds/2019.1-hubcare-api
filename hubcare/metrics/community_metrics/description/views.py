from rest_framework.views import APIView
from rest_framework.response import Response
from description.serializers import DescriptionSerializer
from description.models import Description
import requests
from datetime import datetime, timezone
import os
from community_metrics.function import check_date


class DescriptionView(APIView):
    def get(self, request, owner, repo):

        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not description):

            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo,
                                          auth=(username, token))
            github_data = github_request.json()

            if(github_request.status_code == 200):
                if(github_data['description'] is not None):
                    Description.objects.create(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date_time=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] is None):
                    Description.objects.create(
                        owner=owner,
                        repo=repo,
                        description=False,
                        date_time=datetime.now(timezone.utc)
                    )

        elif(check_date(description)):
            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo,
                                          auth=(username, token))
            github_data = github_request.json()

            if(github_request.status_code is 200):
                if(github_data['description'] is not None):
                    Description.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date_time=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] is None):
                    Description.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=False,
                        date_time=datetime.now(timezone.utc)
                    )

        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serialized = DescriptionSerializer(description, many=True)
        return Response(serialized.data[0])
