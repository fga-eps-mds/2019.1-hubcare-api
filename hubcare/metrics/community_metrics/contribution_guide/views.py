from rest_framework.views import APIView
from rest_framework.response import Response
from contribution_guide.models import ContributionGuide
from contribution_guide.serializers import ContributionGuideSerializer
from datetime import date, datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class ContributionGuideView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a contribution guide or not
        '''
        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not contribution_guide):
            url = '/contents/.github/CONTRIBUTING.md'
            github_request = requests.get(URL_API + owner + '/' + repo + url,
                                          auth=(username, token))

            if(github_request.status_code == HTTP_OK):
                ContributionGuide.objects.create(
                    owner=owner,
                    repo=repo,
                    contribution_guide=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                ContributionGuide.objects.create(
                    owner=owner,
                    repo=repo,
                    contribution_guide=False,
                    date_time=datetime.now(timezone.utc)
                )

        elif(check_date(contribution_guide)):
            url = '/contents/.github/CONTRIBUTING.md'
            github_request = requests.get(URL_API + owner + '/' + repo + url,
                                          auth=(username, token))

            if(github_request.status_code == HTTP_OK):
                ContributionGuide.objects.filter(
                    owner=owner,
                    repo=repo
                    ).update(
                    owner=owner,
                    repo=repo,
                    contribution_guide=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                ContributionGuide.objects.filter(
                    owner=owner,
                    repo=repo
                    ).update(
                    owner=owner,
                    repo=repo,
                    contribution_guide=False,
                    date_time=datetime.now(timezone.utc)
                )

        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )
        contribution_serialized = serialized_object(
            ContributionGuideSerializer,
            contribution_guide
        )
        return Response(contribution_serialized.data[0])
