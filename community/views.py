from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LicenseSerializer
from .models import License
import requests

# Create your views here.

class LicenseView(APIView):
    
    def get(self, request, owner, repo):
        print(repo)
        url = 'https://api.github.com/repos/'
        result = requests.get(url + owner + '/' + repo)
        result = result.json()
        try: 
            if (result['license']) != null:
                return Response(result['license'])
            else:
                return Response(False)
        except:
            raise Http404

      