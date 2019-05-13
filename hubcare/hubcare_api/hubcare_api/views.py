from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from hubcare_api.models import HubcareAPI
from hubcare_api.serializers import HubcareAPISerializer
from rest_framework.response import Response
from hubcare_api.indicators import active_indicator
from hubcare_api.indicators import welcoming_indicator
from hubcare_api.indicators import support_indicator
import requests
import os


class HubcareApiView(APIView):
    def get(self, request, owner, repo):
        '''
        return indicators: active, welcoming and support
        '''
        all_hubcare_api = HubcareAPI.objects.all().filter(
            owner=owner,
            repo=repo
        )

        if (not all_hubcare_api):
            username = os.environ['NAME']
            token = os.environ['TOKEN']
            url = 'https://api.github.com/repos/'
            github_request = requests.get(
                                url + owner + '/' + repo,
                                auth=(username, token)
                            )

            if github_request.status_code == 200:
                active_data = active_indicator.get_active_indicator(
                    owner,
                    repo
                )
                welcoming_data = welcoming_indicator.get_welcoming_indicator(
                    owner,
                    repo
                )
                support_data = support_indicator.get_support_indicator(
                    owner,
                    repo
                )

                HubcareAPI.objects.create(
                    owner=owner,
                    repo=repo,
                    active_indicator=active_data * 100,
                    welcoming_indicator=welcoming_data * 100,
                    support_indicator=support_data * 100,
                )

                hubcare_data = HubcareAPI.objects.all().filter(
                    owner=owner,
                    repo=repo,
                )
                hubcare_serialized = HubcareAPISerializer(
                    hubcare_data,
                    many=True,
                )

                # hubcare_indicators = [
                #     {
                #         "active_indicator": float(
                #             "{0:.2f}".format(active_data*100)),
                #         "welcoming_indicator": float(
                #             "{0:.2f}".format(welcoming_data*100)),
                #         "support_indicator": float(
                #             "{0:.2f}".format(support_data*100)),
                #     }
                # ]

                return Response(hubcare_serialized.data[0])

            else:
                raise Http404
