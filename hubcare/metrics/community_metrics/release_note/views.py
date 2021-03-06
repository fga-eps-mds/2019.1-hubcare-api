from rest_framework.views import APIView
from rest_framework.response import Response
from release_note.models import ReleaseNote
from release_note.serializers import ReleaseNoteSerializer
from datetime import datetime, timedelta, timezone
from community_metrics.constants import URL_API, HTTP_OK, NINETY_DAYS
import requests
import json
import os


class ReleaseNoteView(APIView):

    def get(self, request, owner, repo, token_auth):
        '''
        Return if a repository have a release note or not
        '''
        release_note = ReleaseNote.objects.get(owner=owner, repo=repo)
        serializer = ReleaseNoteSerializer(release_note)
        return Response(serializer.data)

    def post(self, request, owner, repo, token_auth):
        '''
        Post release note object object
        '''
        release_note = ReleaseNote.objects.filter(
            owner=owner,
            repo=repo
        )
        if release_note:
            serializer = ReleaseNoteSerializer(release_note[0])
            return Response(serializer.data)

        release_note = ReleaseNote.objects.create(
            owner=owner,
            repo=repo,
            release_note=check_release_note(owner, repo, token_auth),
        )
        serializer = ReleaseNoteSerializer(release_note)
        return Response(serializer.data)

    def put(self, request, owner, repo, token_auth):
        '''
        Update release note object
        '''
        release_note = ReleaseNote.objects.get(owner=owner, repo=repo)
        release_note.release_note = check_release_note(owner, repo, token_auth)
        release_note.save()

        serializer = ReleaseNoteSerializer(release_note)
        return Response(serializer.data)


def get_github_request(owner, repo, token_auth):
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
    github_request = requests.get(url, headers={'Authorization': 'token ' +
                                  token_auth})
    return github_request.json()


def check_release_note(owner, repo, token_auth):
    '''
    Verify if repository have or not release note
    '''
    github_data = get_github_request(owner, repo, token_auth)
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
