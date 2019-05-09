from rest_framework.views import APIView
from rest_framework.response import Response
from readme.serializers import ReadmeSerializer
from readme.models import Readme
from datetime import datetime, timezone
import requests
import os
from community_metrics.function import check_date, filterObject


class ReadmeView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a readme or not
        '''
        readme = filterObject(Readme)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not readme):
            url = 'https://api.github.com/repos/'
            url2 = '/contents/README.md'
            github_request = requests.get(url + owner + '/' + repo + url2,
                                          auth=(username, token))

            if(github_request.status_code == 200):
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
            url = 'https://api.github.com/repos/'
            url2 = '/contents/README.md'
            github_request = requests.get(url + owner + '/' + repo + url2,
                                          auth=(username, token))

            if(github_request.status_code == 200):
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
        readme_serialized = ReadmeSerializer(readme, many=True)
        return Response(readme_serialized.data[0])
