from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.license_serializer import LicenseSerializer
from community.models.license_model import License
import requests
from datetime import date


class LicenseView(APIView):

    def get(self, request, owner, repo):

        all_license = License.objects.all().filter(owner=owner, repo=repo)

        license_serializer = LicenseSerializer(all_license, many=True)

        if (license_serializer.data == []):

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

        license = License.objects.all().filter(owner=owner, repo=repo)
        license_serialized = LicenseSerializer(license, many=True)
        print(license_serialized.data)
        return Response(license_serialized.data[0])
