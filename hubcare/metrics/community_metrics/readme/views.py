from rest_framework.views import APIView
from rest_framework.response import Response
from readme.serializers import ReadmeSerializer
from readme.models import Readme
from datetime import datetime, timezone
import requests
import os
from community_metrics.constants import URL_API, HTTP_OK


class ReadmeView(APIView):
    def get(self, request, owner, repo):
        '''
        Return if a repository have a readme or not
        '''
        readme = Readme.objects.filter(owner=owner, repo=repo)
        readme_serialized = serialized_object(ReadmeSerializer,  readme)
        return Response(readme_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Create readme object
        '''
        github_request = get_github_request(owner, repo)

        if(github_request.status_code == HTTP_OK):
            response = create_readme(owner, repo, True)
        else:
            response = create_readme(owner, repo, False)
        return Response(response)

    def put(self, request, owner, repo):
        github_request = get_github_request(owner, repo)

        if(github_request.status_code == HTTP_OK):
            response = update_readme(owner, repo, True)
        else:
            response = update_readme(owner, repo, False)
        return Response(response)


def create_readme(owner, repo, value):
    '''
    Create readme object in database
    '''
    Readme.objects.create(
        owner=owner,
        repo=repo,
        readme=value,
        date_time=datetime.now(timezone.utc)
    )
    readme = Readme.objects.filter(owner=owner, repo=repo)
    return serialized_object(ReadmeSerializer,  readme).data[0]


def update_readme(owner, repo, value):
    '''
    Update readme object in database
    '''
    Readme.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        readme=value,
        date_time=datetime.now(timezone.utc)
    )
    readme = Readme.objects.filter(owner=owner, repo=repo)
    return serialized_object(ReadmeSerializer,  readme).data[0]


def get_github_request(owner, repo):
    '''
    Request Github readme
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}/contents/README.md'.format(
        URL_API,
        owner,
        repo
    )
    return requests.get(url, auth=(username, token))
