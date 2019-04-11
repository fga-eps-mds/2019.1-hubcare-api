from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.license_serializer import LicenseSerializer
from community.models.license_model import License
import requests
from datetime import date


class LicenseView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a license or not
        '''
        all_license = License.objects.all().filter(owner=owner, repo=repo)
        # print(all_license[0])
        if (not all_license):

            url = 'https://api.github.com/repos/'
            result = requests.get(url + owner + '/' + repo)
            github_data = result.json()

            if (result.status_code == 404):
                raise Http404
            elif (github_data['license'] != None):
                License.objects.create(
                    owner=owner,
                    repo=repo,
                    have_license=True,
                    date=date.today()
                )
            else:
                License.objects.create(
                    owner=owner,
                    repo=repo,
                    have_license=False,
                    date=date.today()
                )
        elif(check_date(all_license)):
            url = 'https://api.github.com/repos/'
            result = requests.get(url + owner + '/' + repo)
            github_data = result.json()

            if (result.status_code == 404):
                raise Http404
            elif (github_data['license'] != None):
                License.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    have_license=True,
                    date=date.today()
                )
            else:
                License.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    have_license=False,
                    date=date.today()
                )

        license = License.objects.all().filter(owner=owner, repo=repo)
        license_serialized = LicenseSerializer(license, many=True)
        return Response(license_serialized.data[0])


def check_date(license):
    if(license and license[0].date < date.today()):
        return True
    return False
