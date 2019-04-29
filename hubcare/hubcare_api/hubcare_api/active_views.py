from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import *


class ActiveQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo)

        if(github_request.status_code == 200):
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
            
            url_authors = 'acceptance_quality/'
            url = URL_PR + url_authors + owner + '/' + repo
            pr_qua_metric = requests.get(url)
            pr_qua_str = pr_qua_metric.json()[0]['metric']
            pr_qua_float = float(pr_qua_str)

            active_metric = calculate_active_metric(
                release_note_int,
                contributors_int,
                commit_week_int,
                pr_qua_float
            )
        else:
            raise Http404

        data = {"active_metric": active_metric}
        return Response(data)


def calculate_active_metric(
        release_note_int,
        contributors_int,
        commit_week_int,
        pr_qua_float
):
    contributors_int = contributors_int*METRIC_CONTRIBUTOR
    if(contributors_int > 1):
        contributors_int = 1
    active_metric = (
                    release_note_int * HEIGHT_RELESE_NOTE_ACTIVE
                    + contributors_int * HEIGHT_CONTRIBUTOR_ACTIVE
                    + commit_week_int * HEIGHT_COMMIT_WEEK_ACTIVE
                    + pr_qua_float * HEIGHT_PR_QUALITY_1) / ACTIVE_METRIC_QUESTION

    return active_metric
