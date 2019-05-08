from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from readme.serializers import ReadmeSerializer
from readme.models import Readme
import requests
from datetime import date, datetime, timezone
import os


class ReadmeView(APIView):
    def get(self, request, owner, repo):

        readme = Readme.objects.all().filter(owner=owner, repo=repo)

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
                    date=date.today()
                )
            else:
                Readme.objects.create(
                    owner=owner,
                    repo=repo,
                    readme=False,
                    date=date.today()
                )
        elif(check_date(readme)):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/README.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))

            if(github_request.status_code == 200):
                Readme.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    readme=True,
                    date=datetime.now(timezone.utc)
                )
            else:
                Readme.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    readme=False,
                    date=datetime.now(timezone.utc)
                )

        readme = Readme.objects.all().filter(
            owner=owner, repo=repo
        )
        serialized = ReadmeSerializer(
            readme, many=True
        )
        return Response(serialized.data[0])


def check_date(readme_check):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = date.today()
    if(readme_check and (datetime_now - readme_check[0].date).days >= 1):
        return True
    return False
