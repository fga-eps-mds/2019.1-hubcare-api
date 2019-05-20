from rest_framework.views import APIView
from rest_framework.response import Response
from description.serializers import DescriptionSerializer
from description.models import Description
import requests
from datetime import datetime, timezone
import os
from community_metrics.constants import HTTP_OK, URL_API


class DescriptionView(APIView):
    def get(self, request, owner, repo):
        '''
        Return if a repository have a description
        or not
        '''
        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )
        description_serialized = serialized_object(
            DescriptionSerializer,
            description
        )
        return Response(description_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post a new object in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        url = '{0}{1}/{2}'.format(URL_API, owner, repo)
        github_request = requests.get(url, auth=(username, token))
        github_data = github_request.json()

        # if(github_request.status_code == HTTP_OK):
        if(github_data['description'] is not None):
            response = create_description(owner, repo, True)
        else:
            response = create_description(owner, repo, False)
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update description object
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        url = '{0}{1}/{2}'.format(URL_API, owner, repo)
        github_request = requests.get(url, auth=(username, token))
        github_data = github_request.json()

        # if(github_request.status_code is HTTP_OK):
        if(github_data['description'] is not None):
            response = update_description(owner, repo, True)
        elif(github_data['description'] is None):
            response = update_description(owner, repo, False)
        return Response(response)


def create_description(owner, repo, value):
    '''
    Create a decription object in database
    '''
    Description.objects.create(
        owner=owner,
        repo=repo,
        description=value,
        date_time=datetime.now(timezone.utc)
    )
    description = Description.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        DescriptionSerializer,
        description
    ).data[0]


def update_description(owner, repo, value):
    Description.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        description=value,
        date_time=datetime.now(timezone.utc)
    )
    description = Description.objects.filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        DescriptionSerializer,
        description
    ).data[0]
