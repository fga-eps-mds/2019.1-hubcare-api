from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.serializers import ReadmeSerializer
from community.models.readme_model import Readme
import requests
from datetime import date

class ReadmeView(APIView):
    def get(self, request, owner, repo):

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)
        
        if (serialized.data == []):
            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo+ '/readme')
            github_data = github_request.json()

            try:
                if(github_data['documentation_url'] == "https://developer.github.com/v3/repos/contents/#get-the-readme"):
                        Readme.objects.create(
                        owner=owner,
                        repo=repo,
                        readme=False,
                        date=date.today()
                    )
            except:
                print('not found')
            try:
                if(github_data['name'] != None):
                    Readme.objects.create(
                        owner=owner,
                        repo=repo,
                        readme=True,
                        date=date.today()
                    )
            except:
                print('not found')

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)
        print(serialized.data)
        return Response(serialized.data[0])