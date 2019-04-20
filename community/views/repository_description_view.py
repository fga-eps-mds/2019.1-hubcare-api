from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.repository_description_serializer \
    import DescriptionSerializer
from community.models.repository_description_model import RepositoryDescription
import requests
from datetime import datetime, timezone
from hubcareapi.date_check import date_check


class DescriptionView(APIView):
    def get(self, request, owner, repo):

        description = RepositoryDescription.objects.all().filter(
            owner=owner,
            repo=repo
        )

        if (not description):

            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + '/' + repo)

            github_data = github_request.json()

            if(github_request.status_code == 200):
                if(github_data['description'] != None):
                    RepositoryDescription.objects.create(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] == None):
                    RepositoryDescription.objects.create(
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
                    RepositoryDescription.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=True,
                        date=datetime.now(timezone.utc)
                    )
                elif(github_data['description'] == None):
                    RepositoryDescription.objects.filter(
                        owner=owner,
                        repo=repo
                    ).update(
                        owner=owner,
                        repo=repo,
                        description=False,
                        date=datetime.now(timezone.utc)
                    )

        description = RepositoryDescription.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serialized = DescriptionSerializer(description, many=True)
        return Response(serialized.data[0])
