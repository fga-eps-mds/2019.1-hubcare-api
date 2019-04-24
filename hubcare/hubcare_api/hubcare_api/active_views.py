from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import *


class ActiveQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo)

        if(github_request.status_code is 200):
            url = URL_COMMUNITY + 'release_note/' + owner + '/' + repo
            release_note_metric = requests.get(url)
            print(release_note_metric.json())

            url = URL_COMMIT + 'contributors/different_authors/' + owner + '/' + repo
            contributors_metric = requests.get(url)
            print(contributors_metric.json())

            url = URL_COMMIT + 'commit_week/commit_month/' + owner + '/' + repo
            commit_week_metric = requests.get(url)
            print(commit_week_metric.json())

        else:
            raise Http404

        return Response('ok')
