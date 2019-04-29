from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from hubcare_api.indicators import active_indicator
from hubcare_api.indicators import welcoming_indicator
from hubcare_api.indicators import support_indicator
import requests
import os


class HubcareApiView(APIView):
    def get(self, request, owner, repo):
        username = os.environ['NAME']
        token = os.environ['TOKEN']
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo,
                                      auth=(username, token))

        if github_request.status_code == 200:
            active_data = active_indicator.get_active_indicator(owner, repo)
            welcoming_data = welcoming_indicator.get_welcoming_indicator(
                owner,
                repo
            )
            support_data = support_indicator.get_support_indicator(owner, repo)
            hubcare_indicators = [
                {
                    "active_indicator": float(
                        "{0:.2f}".format(active_data*100)),
                    "welcoming_indicator": float(
                        "{0:.2f}".format(welcoming_data*100)),
                    "support_indicator": float(
                        "{0:.2f}".format(support_data*100)),
                }
            ]

            return Response(hubcare_indicators)
        else:
            raise Http404
