from rest_framework.views import APIView
from rest_framework.response import Response
from description.serializers import DescriptionSerializer
from description.models import Description
import requests
from datetime import datetime, timezone
import os
from community_metrics.functions \
    import check_date, serialized_object
from community_metrics.constants import HTTP_OK, URL_API


class DescriptionView(APIView):
    def get(self, request, owner, repo):

        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not description):

            github_request = requests.get(URL_API + owner + '/' + repo,
                                          auth=(username, token))
            github_data = github_request.json()

            if(github_request.status_code == HTTP_OK):
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
            github_request = requests.get(URL_API + owner + '/' + repo,
                                          auth=(username, token))
            github_data = github_request.json()

            if(github_request.status_code is HTTP_OK):
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
        description_serialized = serialized_object(
            DescriptionSerializer,
            description
        )
        return Response(description_serialized.data[0])
