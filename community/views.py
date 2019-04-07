from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReadmeSerializer
from .models import Readme
import requests
from datetime import date

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
        result = requests.get(url + owner + '/' + repo + '/contents/README.md')
        result = result.json()

        try:
            if(result['size'] > 50):
                return Response(True)

        except:
            return Response(False)