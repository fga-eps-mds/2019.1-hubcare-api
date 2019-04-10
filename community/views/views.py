from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.serializers import ReadmeSerializer
from community.models.models import Readme
import requests
from datetime import date

class ReadmeView(APIView):
    def get(self, request, owner, repo):

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)
        
        if (serialized.data == []): #não sei o por quê
            print('existe!!!')
            
            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo)
            github_data = github_request.json()

            #'/contents/README.md'

            print('passei aqui - 1')
            
        
            if(github_request.status_code == 404):
                raise Http404
            if(github_data.status_code == 200):
                print('passei aqui - 2')
                if(github_data['readme'] != None):
                    Readme.objects.create(
                        owner=owner,
                        repo=repo,
                        readme=True,
                        data=date.now()
                    )
                else:
                    Readme.objects.create(
                        owner=owner,
                        repo=repo,
                        readme=False,
                        data=date.now()
                    )
        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)
        print(serialized.data)
        return Response(serialized.data[0])