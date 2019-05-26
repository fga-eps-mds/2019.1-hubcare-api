from rest_framework import status
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
        readme = Readme.objects.get(owner=owner, repo=repo)
        serializer = ReadmeSerializer(readme)
        return Response(serializer.data)

    def post(self, request, owner, repo):
        '''
        Create readme object
        '''
        readme = Readme.objects.filter(
            owner=owner,
            repo=repo
        )
        if readme:
            serializer = ReadmeSerializer(readme[0])
            return Response(serializer.data)

        github_request = get_github_request(owner, repo)
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = create_readme(owner, repo, True)
        elif status_code == 404:
            response = create_readme(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)

    def put(self, request, owner, repo):
        github_request = get_github_request(owner, repo)
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = update_readme(owner, repo, True)
        elif status_code == 404:
            response = update_readme(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)


def create_readme(owner, repo, value):
    '''
    Create readme object in database
    '''
    readme = Readme.objects.create(
        owner=owner,
        repo=repo,
        readme=value,
    )
    serializer = ReadmeSerializer(readme)
    return serializer.data


def update_readme(owner, repo, value):
    '''
    Update readme object in database
    '''
    readme = Readme.objects.get(owner=owner, repo=repo)
    readme.readme = value
    readme.save()

    serializer = ReadmeSerializer(readme)
    return serializer.data


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
