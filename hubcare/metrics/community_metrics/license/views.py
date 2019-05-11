from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from license.serializers import LicenseSerializer
from license.models import License
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions \
 import check_date, filter_object, serialized_object
from community_metrics.constants import URL_API, HTTP_OK, HTTP_NOT_FOUND


class LicenseView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a license or not
        '''
        all_license = filter_object(License)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not all_license):
            result = requests.get(URL_API + owner + '/' + repo,
                                  auth=(username, token))

            github_data = result.json()

            if (result.status_code == HTTP_NOT_FOUND):
                raise Http404
            elif (github_data['license'] is not None):
                License.objects.create(
                    owner=owner,
                    repo=repo,
                    have_license=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                License.objects.create(
                    owner=owner,
                    repo=repo,
                    have_license=False,
                    date_time=datetime.now(timezone.utc)
                )
        elif(check_date(all_license)):
            result = requests.get(URL_API + owner + '/' + repo,
                                  auth=(username, token))

            github_data = result.json()

            if (result.status_code == HTTP_NOT_FOUND):
                raise Http404
            elif (github_data['license'] is not None):
                License.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    have_license=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                License.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    have_license=False,
                    date_time=datetime.now(timezone.utc)
                )

        license = License.objects.all().filter(owner=owner, repo=repo)
        license_serialized = serialized_object(LicenseSerializer, license)
        return Response(license_serialized.data[0])
