from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReadmeSerializer
from .models import Readme
import requests
from datetime import date

'''
class ReadmeView(APIView):

    def get(self, request, owner, repo):

        readme = Readme.objects.all()
        serializer = ReadmeSerializer(readme, many=True)
        return Response(serializer.data)

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        if (readme):
            print('tem readme')
        else:
            #Readme.objects.create(owner=owner, repo=repo, date=date.today())
            print('falhou')
        
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo + '/contents/README.md')
        github_request = github_request.json()

        try:
            if(result['size'] > 50):
                return Response(True)

        except:
            return Response(False)
'''
class ReadmeView(APIView):
    def get(self, request, owner, repo):
        readme = Readme.objects.all().filter(owner=owner, repo=repo)

        # readme_serialized = ReadmeSerializer(readme, many=True)
        if(readme == []):
            # if readme[0].readme == True:
            github_request = requests.get("https://api.github.com/repos/" + \
                owner + "/" + repo + "/contents/README.md")
            print(github_request.json())
            if((github_request.status_code == 200) and (result['size'] > 30)):
                Readme.objects.create(owner=owner, repo=repo, readme=True, date=datetime.now())
            else:
                Readme.objects.create(owner=owner, repo=repo, readme=False)
        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        readme_serialized = ReadmeSerializer(readme, many=True)
        return Response(readme_serialized.data)