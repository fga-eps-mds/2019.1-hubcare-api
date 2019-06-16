from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from license.serializers import LicenseSerializer
from license.models import License
from datetime import datetime, timezone
import requests
import os
from community_metrics.constants import URL_API, HTTP_OK, HTTP_NOT_FOUND


class LicenseView(APIView):
    def get(self, request, owner, repo, token_auth):
        '''
        Return if a repository have a license or not
        '''
        license = License.objects.get(owner=owner, repo=repo)
        serializer = LicenseSerializer(license)
        return Response(serializer.data)

    def post(self, request, owner, repo, token_auth):
        '''
        Post a new license object
        '''
        license = License.objects.filter(
            owner=owner,
            repo=repo
        )
        if license:
            serializer = LicenseSerializer(license[0])
            return Response(serializer.data)

        github_data = get_github_request(owner, repo, token_auth)
        if (github_data['license'] is not None):
            response = create_license(owner, repo, token_auth, True)
        else:
            response = create_license(owner, repo, token_auth, False)
        return Response(response)

    def put(self, request, owner, repo, token_auth):
        '''
        Update license object
        '''
        github_data = get_github_request(owner, repo, token_auth)
        if (github_data['license'] is not None):
            response = update_license(owner, repo, token_auth, True)
        else:
            response = update_license(owner, repo, token_auth, False)
        return Response(response)


def create_license(owner, repo, token_auth, value):
    '''
    Create license object
    '''
    license = License.objects.create(
        owner=owner,
        repo=repo,
        license=value,
    )
    serializer = LicenseSerializer(license)
    return serializer.data


def update_license(owner, repo, token_auth, value):
    '''
    Update license object
    '''
    license = License.objects.get(owner=owner, repo=repo)
    license.license = value
    license.save()
    serializer = LicenseSerializer(license)
    return serializer.data


def get_github_request(owner, repo, token_auth):
    '''
    Request github repository data
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}'.format(URL_API, owner, repo, token_auth)
    result = requests.get(url, headers={'Authorization': 'token ' + token_auth})

    return result.json()
