from rest_framework.views import APIView
from rest_framework.response import Response
from readme.serializers import ReadmeSerializer
from readme.models import Readme
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class ReadmeView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a readme or not
        '''
        readme = Readme.objects.all().filter(owner=owner, repo=repo)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not readme):
            url = '/contents/README.md'
            github_request = requests.get(URL_API + owner + '/' + repo + url,
                                          auth=(username, token))

            if(github_request.status_code == HTTP_OK):
                Readme.objects.create(
                    owner=owner,
                    repo=repo,
                    readme=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                Readme.objects.create(
                    owner=owner,
                    repo=repo,
                    readme=False,
                    date_time=datetime.now(timezone.utc)
                )

        elif(check_date(readme)):
            url = '/contents/README.md'
            github_request = requests.get(URL_API + owner + '/' + repo + url,
                                          auth=(username, token))

            if(github_request.status_code == HTTP_OK):
                Readme.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    readme=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                Readme.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    readme=False,
                    date_time=datetime.now(timezone.utc)
                )

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        readme_serialized = serialized_object(ReadmeSerializer,  readme)
        return Response(readme_serialized.data[0])
