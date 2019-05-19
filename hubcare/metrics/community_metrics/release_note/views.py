from rest_framework.views import APIView
from rest_framework.response import Response
from release_note.models import ReleaseNote
from release_note.serializers import ReleaseNoteSerializer
from datetime import datetime, timedelta, timezone
from community_metrics.functions import serialized_object
from community_metrics.constants import URL_API, HTTP_OK, NINETY_DAYS
import requests
import json
import os


class ReleaseNoteView(APIView):

    def get(self, request, owner, repo):
        '''
        Return if a repository have a release note or not
        '''
        readme = ReleaseNote.objects.filter(owner=owner, repo=repo)
        readme_serialized = serialized_object(ReleaseNoteSerializer,  readme)
        return Response(readme_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post release note object object
        '''
        ReleaseNote.objects.create(
            owner=owner,
            repo=repo,
            have_realease_note=check_release_note(owner, repo),
            date=datetime.now(timezone.utc)
        )
        release = ReleaseNote.objects.filter(owner=owner, repo=repo)
        response = serialized_object(
            ReleaseNoteSerializer,
            release
        ).data[0]
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update release note object
        '''
        ReleaseNote.objects.filter(owner=owner, repo=repo).update(
            owner=owner,
            repo=repo,
            have_realease_note=check_release_note(owner, repo),
            date=datetime.now(timezone.utc)
        )
        release = ReleaseNote.objects.filter(owner=owner, repo=repo)
        response = serialized_object(
            ReleaseNoteSerializer,
            release
        ).data[0]
        return Response(response)


def get_github_request(owner, repo):
    '''
    Request Github release notes
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}/releases'.format(
        URL_API,
        owner,
        repo
    )
    github_request = requests.get(url, auth=(username, token))
    return github_request.json()


def check_release_note(owner, repo):
    '''
    Verify if repository have or not release note
    '''
    github_data = get_github_request(owner, repo)
    present = datetime.today()
    days = timedelta(days=NINETY_DAYS)
    releaseDays = present - days
    has_release_note = False
    if(github_data != []):
        releaseDate = datetime.strptime(
            github_data[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        if(releaseDate > releaseDays):
            has_release_note = True
    return has_release_note
