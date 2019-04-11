from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from issues.models.help_wanted_models import HelpWanted
from issues.serializers.help_wanted_serializers import HelpWantedSerializer

# Create your views here.

class HelpWantedView(APIView):
    def get(self,request,owner,repo):
        return Response(owner)
        

