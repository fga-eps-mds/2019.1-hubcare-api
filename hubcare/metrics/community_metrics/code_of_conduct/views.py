from rest_framework.views import APIView
from rest_framework.response import Response
from code_of_conduct.models import CodeOfConduct
from code_of_conduct.serializers import CodeOfConductSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class CodeOfConductView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository has a code of conduct or not
        '''
        code_of_conduct = CodeOfConduct.objects.filter(
            owner=owner,
            repo=repo
        )
        code_of_conduct_serialized = serialized_object(
            CodeOfConductSerializer,
            code_of_conduct
        )

        return Response(code_of_conduct_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post a new object in database
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
        if(github_request.status_code == HTTP_OK):
            response = create_object(owner, repo, True)
        else:
            response = create_object(owner, repo, False)
        return Response(response)

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
        if(github_request.status_code == HTTP_OK):
            response = update_object(owner, repo, True)
        else:
            response = update_object(owner, repo, False)
        return Response(response)


def create_object(owner, repo, code_of_conduct):
    '''
    Create code of conduct object in database
    '''
    CodeOfConduct.objects.create(
        owner=owner,
        repo=repo,
        code_of_conduct=code_of_conduct,
        date_time=datetime.now(timezone.utc)
    )
    code_of_conduct = CodeOfConduct.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        CodeOfConductSerializer,
        code_of_conduct
    ).data[0]


def update_object(owner, repo, code_of_conduct):
    '''
    Update code of conduct object in database
    '''
    CodeOfConduct.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        code_of_conduct=code_of_conduct,
        date_time=datetime.now(timezone.utc)
    )
    code_of_conduct = CodeOfConduct.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        CodeOfConductSerializer,
        code_of_conduct
    ).data[0]
