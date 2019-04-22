from rest_framework.views import APIView
from rest_framework.response import Response
from description.serializers import DescriptionSerializer
from description.models import Description
import requests
from datetime import datetime, timezone


class DescriptionView(APIView):
    def get(self, request, owner, repo):

        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )

        if (not description):

            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo)

            github_data = github_request.json()

            if(github_request.status_code == 200):
                if(github_data['description'] != None):
                    Description.objects.create(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] == None):
                    Description.objects.create(
                        owner=owner,
                        repo=repo,
                        description=False,
                        date=datetime.now(timezone.utc)
                    )
        elif(date_check(description)):
            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo)
            github_data = github_request.json()

            if(github_request.status_code == 200):
                if(github_data['description'] != None):
                    Description.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] == None):
                    Description.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=False,
                        date=datetime.now(timezone.utc)
                    )

        description = Description.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serialized = DescriptionSerializer(description, many=True)
        return Response(serialized.data[0])


def date_check(tested_variable):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(tested_variable and (datetime_now - tested_variable[0].date).days >= 1):
        return True
    return False
