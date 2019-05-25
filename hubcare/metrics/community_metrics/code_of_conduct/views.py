from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from code_of_conduct.models import CodeOfConduct
from code_of_conduct.serializers import CodeOfConductSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.constants import URL_API, HTTP_OK


class CodeOfConductView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository has a code of conduct or not
        '''
        code_of_conduct = CodeOfConduct.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = CodeOfConductSerializer(code_of_conduct)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):
        '''
        Post a new object in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        code_of_conduct = CodeOfConduct.objects.filter(
            owner=owner,
            repo=repo
        )
        if code_of_conduct:
            serializer = CodeOfConductSerializer(code_of_conduct[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        result = '{0}{1}/{2}/contents/.github/CODE_OF_CONDUCT.md'.format(
            URL_API,
            owner,
            repo
        )

        github_request = requests.get(
            result,
            auth=(username, token)
        )
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = create_object(owner, repo, True)
        elif status_code == 404:
            response = create_object(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, owner, repo):
        '''
        Update object values in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        result = '{0}{1}/{2}/contents/.github/CODE_OF_CONDUCT.md'.format(
            URL_API,
            owner,
            repo
        )
        github_request = requests.get(
            result,
            auth=(username, token)
        )
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = update_object(owner, repo, True)
        elif status_code == 404:
            response = update_object(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)


def create_object(owner, repo, code_of_conduct):
    '''
    Create code of conduct object in database
    '''
    code_of_conduct = CodeOfConduct.objects.create(
        owner=owner,
        repo=repo,
        code_of_conduct=code_of_conduct,
        date_time=datetime.now(timezone.utc)
    )
    serializer = CodeOfConductSerializer(code_of_conduct)
    return serializer.data


def update_object(owner, repo, code_of_conduct):
    '''
    Update code of conduct object in database
    '''
    code_of_conduct_object = CodeOfConduct.objects.get(
        owner=owner,
        repo=repo
    )
    code_of_conduct_object.code_of_conduct = code_of_conduct
    code_of_conduct_object.save()
    serializer = CodeOfConductSerializer(code_of_conduct_object)
    return serializer.data
