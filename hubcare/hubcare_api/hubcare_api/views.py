from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import *
import os
from hubcare_api import active_indicator


class HubcareApiView(APIView):
    def get(self, request, owner, repo):
        data = active_indicator.get_active_indicator(owner, repo)

        return Response(data)
