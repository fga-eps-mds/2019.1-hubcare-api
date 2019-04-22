from rest_framework.views import APIView
from rest_framework.response import Response
from contribution_guide.models import ContributionGuide
from contribution_guide.serializers import ContributionGuideSerializer
from datetime import date
import requests


class ContributionGuideView(APIView):

    def get(self, request, owner, repo):
        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serialized = ContributionGuideSerializer(contribution_guide, many=True)

        if(serialized.data == []):

            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/CONTRIBUTING.md'
            github_request = requests.get(url1 + owner + '/' + repo + url2)

            if(github_request.status_code == 200):
                ContributionGuide.objects.create(
                    owner=owner,
                    repo=repo,
                    contribution_guide=True,
                    date=date.today()
                )
            else:
                ContributionGuide.objects.create(
                    owner=owner,
                    repo=repo,
                    contribution_guide=False,
                    date=date.today()
                )

        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serialized = ContributionGuideSerializer(contribution_guide, many=True)
        return Response(serialized.data)
