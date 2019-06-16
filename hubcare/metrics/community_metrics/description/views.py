from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from description.serializers import DescriptionSerializer
from description.models import Description
import requests
from datetime import datetime, timezone
import os
from community_metrics.constants import HTTP_OK, URL_API


class DescriptionView(APIView):
    def get(self, request, owner, repo, token_auth):
        '''
        Return if a repository have a description
        or not
        '''
        description = Description.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = DescriptionSerializer(description)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo, token_auth):
        '''
        Post a new object in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        description = Description.objects.filter(
            owner=owner,
            repo=repo
        )
        if description:
            serializer = DescriptionSerializer(description[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = '{0}{1}/{2}'.format(URL_API, owner, repo, token_auth)
        github_request = requests.get(url, headers={'Authorization': 'token ' +
                                      token_auth})
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            github_data = github_request.json()
            if(github_data['description'] is not None):
                response = create_description(owner, repo, token_auth, True)
            else:
                response = create_description(owner, repo, token_auth, False)
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner, repo, token_auth):
        '''
        Update description object
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        url = '{0}{1}/{2}'.format(URL_API, owner, repo, token_auth)
        github_request = requests.get(url, headers={'Authorization': 'token ' +
                                      token_auth})
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            github_data = github_request.json()
            if(github_data['description'] is not None):
                response = update_description(owner, repo, token_auth, True)
            else:
                response = update_description(owner, repo, token_auth, False)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)


def create_description(owner, repo, token_auth, value):
    '''
    Create a decription object in database
    '''
    description = Description.objects.create(
        owner=owner,
        repo=repo,
        description=value,
    )
    serializer = DescriptionSerializer(description)
    return serializer.data


def update_description(owner, repo, token_auth, value):
    description = Description.objects.get(owner=owner, repo=repo)
    description.description = value
    description.save()
    serializer = DescriptionSerializer(description)
    return serializer.data
