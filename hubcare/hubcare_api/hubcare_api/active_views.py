from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import *


class ActiveQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo)

        if(github_request.status_code is 200):
            url = URL_COMMUNITY + 'release_note/' + owner + '/' + repo
            release_note_metric = requests.get(url)
            release_note_bool = release_note_metric.json()['response']
            release_note_int = int(release_note_bool)

            url_authors = 'contributors/different_authors/'
            url = URL_COMMIT + url_authors + owner + '/' + repo
            contributors_metric = requests.get(url)
            contributors_total = len(contributors_metric.json())
            contributors_int = int(contributors_total)

            url = URL_COMMIT + 'commit_week/commit_month/' + owner + '/' + repo
            commit_week_metric = requests.get(url)
            commit_week_sum = commit_week_metric.json()['sum']
            commit_week_int = int(commit_week_sum)

            active_metric = calculate_active_metric(
                release_note_int,
                contributors_int,
                commit_week_int
            )
        else:
            raise Http404

        return Response(active_metric)


def calculate_active_metric(
        release_note_int,
        contributors_int,
        commit_week_int
):
    contributors_int = contributors_int*METRIC_CONTRIBUTOR
    if(contributors_int > 1):
        contributors_int = 1
    active_metric = (
                    release_note_int*HEIGHT_RELESE_NOTE_ACTIVE
                    + contributors_int*HEIGHT_CONTRIBUTOR_ACTIVE
                    + commit_week_int*HEIGHT_COMMIT_WEEK_ACTIVE)/10

    return active_metric
