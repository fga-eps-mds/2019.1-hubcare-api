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
        '''
        return if a repository have a readme or not
        '''
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


def check_date(readme):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(readme and (datetime_now - readme[0].date_time).days >= 1):
        return True
    return False
