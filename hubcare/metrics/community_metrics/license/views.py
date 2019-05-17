from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from license.serializers import LicenseSerializer
from license.models import License
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK, HTTP_NOT_FOUND


class LicenseView(APIView):
    def get(self, request, owner, repo):
        '''
        Return if a repository have a license or not
        '''
        license = License.objects.all().filter(owner=owner, repo=repo)
        license_serialized = serialized_object(LicenseSerializer, license)
        return Response(license_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post a new license object
        '''
        github_data = get_github_request(owner, repo)

        if (github_data['license'] is not None):
            response = create_license(owner, repo, True)
        else:
            response = create_license(owner, repo, False)
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update license object
        '''
        github_data = get_github_request(owner, repo)

        if (github_data['license'] is not None):
            response = update_license(owner, repo, True)
        else:
            response = update_license(owner, repo, False)
        return Response(response)


def create_license(owner, repo, value):
    '''
    Create license object
    '''
    License.objects.create(
        owner=owner,
        repo=repo,
        have_license=value,
        date_time=datetime.now(timezone.utc)
    )
    license = License.objects.filter(owner=owner, repo=repo)
    return serialized_object(LicenseSerializer, license).data[0]


def update_license(owner, repo, value):
    '''
    Update license object
    '''
    License.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        have_license=value,
        date_time=datetime.now(timezone.utc)
    )
    license = License.objects.filter(owner=owner, repo=repo)
    return serialized_object(LicenseSerializer, license).data[0]


def get_github_request(owner, repo):
    '''
    Request github repository data
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}'.format(URL_API, owner, repo)
    result = requests.get(url, auth=(username, token))

    return result.json()
