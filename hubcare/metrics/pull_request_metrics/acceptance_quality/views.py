import requests
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PullRequestQuality
from .serializers import PullRequestQualitySerializers
from datetime import datetime, timezone
from acceptance_quality.constants import *
import os


class PullRequestQualityView(APIView):
    '''
        Check the quality of a pull request, based on metrics
        Input: owner, repo
        Output: Response calculated based on metrics
    '''
    def get(self, request, owner, repo):
        '''
            Check the existence of pull requests validate
            and fix it according to metrics
            Input: owner, repo
            Output: the quality of the PRs based on the metrics
        '''
        pull_request_quality = PullRequestQuality.objects.all().filter(
            owner=owner, repo=repo)
        pull_request_qualityserialized = PullRequestQualitySerializers(
            pull_request_quality, many=True)

        if(not pull_request_quality):
            PullRequestQuality.objects.create(
                owner=owner,
                repo=repo,
                date=datetime.now(timezone.utc),
                metric=get_pull_request(owner, repo)
            )
        elif check_datetime(pull_request_quality[0]):
            PullRequestQuality.objects.filter(owner=owner, repo=repo).update(
                date=datetime.now(timezone.utc),
                metric=get_pull_request(owner, repo)
            )

        pull_request_quality = PullRequestQuality.objects.all().filter(
            owner=owner, repo=repo)

        pull_request_quality = PullRequestQualitySerializers(
            pull_request_quality, many=True)

        return Response(pull_request_quality.data)


def check_datetime(pull_request):
    '''
    Verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - pull_request.date).days >= 1):
        return True
    return False


def check_datetime_days(pull_request, days):
    '''
    Verifies if the time difference between the issue created and now is
    greater than X days
    '''
    pull_request = datetime.strptime(pull_request, '%Y-%m-%dT%H:%M:%SZ')
    datetime_now = datetime.now()
    if((datetime_now - pull_request).days <= days):
        return True
    return False


def get_pull_request(owner, repo):
    '''
    Get all the PRs in the last 60 days or the first 50 PRs
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    page_number = 1
    pull_request_score = 0
    elements = 0
    url = 'https://api.github.com/repos/' + owner + '/' + repo + \
          '/' + 'pulls?state=all&page='
    aux = True
    while aux:
        github_request = requests.get(url + str(page_number) + '&per_page=100',
                                      auth=(username, token))
        github_data = github_request.json()

        if (github_data == [] and elements == 0):
            return 0

        for pr in github_data:
            if(check_datetime_days(pr['created_at'], NUM_PRS) and
                    elements < LAST_PRS):
                score = calculate_metric(owner, repo, pr)
                print("score = ", score)
                pull_request_score = pull_request_score + score
                print("pull_request_score =", pull_request_score)
                elements = elements + 1
            elif(elements < LAST_PRS):
                score = calculate_metric(owner, repo, pr)
                print("score = ", score)
                pull_request_score = pull_request_score + score
                print("pull_request_score =", pull_request_score)
                elements = elements + 1
            else:
                # Do nothing
                pass
            print("elementos = ", elements)
        if(github_data == []):
            aux = False
        if(elements == LAST_PRS):
            aux = False
        page_number = page_number + 1
    print("pull_request_score_total =", pull_request_score)
    pull_request_score = pull_request_score / elements
    print("elements =", elements)
    return pull_request_score


def calculate_metric(owner, repo, pr):
    '''
        Calculate metric

        Status  |Have discussion  |Result
        Merged  |Yes              |1
        Merged  |No               |0.9
        Open    |Recent(<=15 days)|0.9
        Closed  |Yes              |0.7
         (without Merge)
        Open (Older (>15 days))   |0.3
        Closed  |No               |0.1
         (without Merge)
        Open |No (old)            |0
    '''
    comments = get_comments(owner, repo, pr['number'])

    if pr['merged_at'] is not None and comments >= 1:
        score = 1
        print("Merged with discussio")
    elif pr['merged_at'] is not None and comments == 0:
        score = 0.9
        print("Merged without discussion")
    elif pr['state'] == 'open' and check_datetime_days(pr['updated_at'], 15):
        score = 0.9
        print("Open with recent discussion")
    elif pr['state'] == 'closed' and comments >= 1:
        print("Closed with discussion")
        score = 0.7
    elif pr['state'] == 'open' and not check_datetime_days(pr['updated_at'],
                                                           15):
        print("Open with old discussion")
        score = 0.3
    elif pr['state'] == 'closed' and comments == 0:
        print("Closed without discussion")
        score = 0.1
    elif pr['state'] == 'open' and comments == 0:
        print("Open without discussion")
        score = 0
    return score


def get_comments(owner, repo, number):
    '''
    Get all the comments
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    url = 'https://api.github.com/repos/'
    github_request = requests.get(
        url + owner + '/' + repo + '/pulls' + '/' + str(number),
        auth=(username, token))
    github_data = github_request.json()

    comments = github_data['comments'] + github_data['review_comments']
    print("comments = ", comments)

    return comments
