from rest_framework.views import APIView
from rest_framework.response import Response
from contribution_guide.models import ContributionGuide
from contribution_guide.serializers import ContributionGuideSerializer
from datetime import date, datetime, timezone
import requests
import os


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
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/CONTRIBUTING.md'
            github_request = requests.get(url1 + owner + '/' + repo + url2,
                                          auth=(username,
                                                token))

            if(github_request.status_code == 200):
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
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/CONTRIBUTING.md'
            github_request = requests.get(url1 + owner + '/' + repo + url2,
                                          auth=(username,
                                                token))

            github_request = requests.get(url + owner + '/' + repo + url2,
                                          auth=(username, token))

            if(github_request.status_code == 200):
                Readme.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    contribution_guide=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                Readme.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    contribution_guide=False,
                    date_time=datetime.now(timezone.utc)
                )

        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )
        contribution_serialized = ContributionGuideSerializer(
            contribution_guide,
            many=True
        )
        return Response(contribution_serialized.data[0])


def check_date(contribution):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(contribution and (datetime_now - contribution[0].date_time).days >= 1):
        return True
    return False
