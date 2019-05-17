from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from repository.models import Repository
from repository.serializers import RepositorySerializer
from repository import constants
import requests
import json
import os

STATUS = {
    '0': 'Repository does not exist',
    '1': 'Repository needs to be created',
    '2': 'Repository needs to be updated',
    '3': 'Repository is already updated',
}


class RepositoryView(APIView):
    def get(self, request, owner, repo):
        '''
        Checks the existence of a repository and the last time it was updated
        '''
        repository = Repository.objects.filter(owner=owner, repo=repo)
        url = constants.MAIN_URL + owner + '/' + repo

        '''
        Checks if there's a repository in database
        '''
        if not repository:
            username = os.environ['NAME']
            token = os.environ['TOKEN']
            data = requests.get(url, auth=(username, token))

            '''
            Executes if repository exists
            '''
            if data.status_code >= 200 and data.status_code < 300:
                response = create_response(1)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = create_response(0)
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        elif check_datetime(repository[0]):
            response = create_response(2)
            return Response(response, status.HTTP_200_OK)
        else:
            response = create_response(3)
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):
        repository = {
            'repo': repo,
            'owner': owner,
            'date': datetime.now(timezone.utc)
        }
        serializer = RepositorySerializer(data=repository)
        if serializer.is_valid():
            serializer.save()
            return Response('Repository added', status=status.HTTP_201_CREATED)
        else:
            return Response('Repository data is invalid', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner, repo):
        repository = Repository.objects.filter(owner=owner, repo=repo)
        try:
            repository.update(date=datetime.now(timezone.utc))
            return Response('Repository successfully updated', status=status.HTTP_200_OK)
        except:
            return Response('Error on updating status', status=status.HTTP_400_BAD_REQUEST)

def check_datetime(object_date):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - object_date.date).days >= constants.ONE_DAY):
        return True
    return False

def create_response(status):
    response = {
        'status': status,
        'message': STATUS[str(status)],
    }
    return response