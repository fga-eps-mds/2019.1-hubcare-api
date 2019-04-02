from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LicenseSerializer
from .models import License
import requests

# Create your views here.

class LicenseView(APIView):
    
    def get(self, request):

        result = requests.get('https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api')
        result = result.json()

        licenses =  License.objects.all()
        serializer = LicenseSerializer(licenses, many=True)

        return Response(serializer.data)