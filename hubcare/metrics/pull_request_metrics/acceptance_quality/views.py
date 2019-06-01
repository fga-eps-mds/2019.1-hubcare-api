import requests
import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from acceptance_quality.models import PullRequestQuality
from acceptance_quality.serializers import PullRequestQualitySerializer
from datetime import datetime, timezone, timedelta
from pull_request_metrics.constants import TOTAL_DAYS, URL_PR, TOTAL_PR, \
                                           LAST_UPDATED_TIME
import os
import json


class PullRequestQualityView(APIView):
    def get(self, request, owner, repo):
        '''
        Returns the quality of the pull
        requests from the repository
        '''

        pr_quality = PullRequestQuality.objects.get(owner=owner, repo=repo)
        serializer = PullRequestQualitySerializer(pr_quality)
        custom_serializer = customize_serializer(serializer.data)
        return Response(custom_serializer)

    def post(self, request, owner, repo):
        '''
        Post a new quality of the pull
        requests from the repository
        '''

        pr_quality = PullRequestQuality.objects.filter(
            owner=owner,
            repo=repo
        )
        if pr_quality:
            serializer = PullRequestQualitySerializer(pr_quality[0])
            custom_serializer = customize_serializer(serializer.data)
            return Response(custom_serializer)

        updated, merged = get_pull_requests(owner, repo)
        if updated is not None:
            metric = get_metric(updated, merged)
        else:
            return Response('Error on requesting GitHub API',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pr_quality = PullRequestQuality.objects.create(
            owner=owner,
            repo=repo,
            acceptance_rate=metric['acceptance_rate'],
            categories=json.dumps(metric['categories'])
        )
        serializer = PullRequestQualitySerializer(pr_quality)

        custom_serializer = customize_serializer(serializer.data)
        return Response(custom_serializer)

    def put(self, request, owner, repo):
        '''
        Update a quality of the pull requests
        from the repository
        '''

        updated, merged = get_pull_requests(owner, repo)
        if updated is not None:
            metric = get_metric(updated, merged)
        else:
            return Response('Error on requesting GitHub API',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pr_quality = PullRequestQuality.objects.get(owner=owner, repo=repo)
        pr_quality.acceptance_rate = metric['acceptance_rate']
        pr_quality.categories = json.dumps(metric['categories'])
        pr_quality.save()

        serializer = PullRequestQualitySerializer(pr_quality)
        custom_serializer = customize_serializer(serializer.data)

        return Response(custom_serializer)


def customize_serializer(data):
    custom_serializer = {}
    custom_serializer.update(data)
    categories_json = json.loads(custom_serializer['categories'])
    custom_serializer['categories'] = categories_json
    return custom_serializer


def get_pull_requests(owner, repo):
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    interval = timedelta(days=TOTAL_DAYS)
    date = str(datetime.now() - interval).split(' ')[0]

    url_updated = URL_PR + '+updated:>=' + date + \
        '+repo:' + owner + '/' + repo + \
        '&per_page=100'
    updated_request = requests.get(url_updated, auth=(username, token))
    updated_status = updated_request.status_code

    url_merged = url_updated.replace('updated', 'merged')
    merged_request = requests.get(url_merged, auth=(username, token))
    merged_status = merged_request.status_code

    updated = []
    merged = []
    if updated_status != merged_status:
        return None, None
    elif updated_status >= 200 and updated_status < 300:
        updated = updated_request.json()['items']
        merged = merged_request.json()['items']
        return updated, merged
    elif updated_status == 422:
        return updated, merged
    else:
        return None, None


def get_metric(updated, merged):
    '''
    Calculate pull request quality metric

    Situation	Discussion	Result

    Merged      Yes	        1
    Merged	    No	        0.9
    Open    (<=15 days)	    0.9
    Closed and without merged	Yes     0.7
    Open	(>15 days)	    0.3
    Closed and without merged	No	0.1
    Open      No/old        0
    '''

    pr_number = 0
    total_score = 0
    merged_pos = 0
    merged_size = len(merged)
    categories = {
        'merged_yes': 0,
        'merged_no': 0,
        'open_yes_new': 0,
        'closed_yes': 0,
        'open_yes_old': 0,
        'closed_no': 0,
        'open_no_old': 0
    }

    for i in updated:
        if pr_number >= TOTAL_PR:
            break
        elif merged_pos < merged_size and i['id'] == merged[merged_pos]['id']:
            if i['comments'] > 0:
                total_score += 1
                categories['merged_yes'] += 1
            else:
                total_score += 0.9
                categories['merged_no'] += 1
            merged_pos += 1
        elif i['state'] == 'closed':
            if i['comments'] > 0:
                total_score += 0.7
                categories['closed_yes'] += 1
            else:
                total_score += 0.1
                categories['closed_no'] += 1
        elif i['comments'] > 0:
            if check_datetime(i['updated_at']):
                total_score += 0.9
                categories['open_yes_new'] += 1
            else:
                total_score += 0.3
                categories['open_yes_old'] += 1
        else:
            categories['open_no_old'] += 1
        pr_number += 1

    if pr_number == 0:
        acceptance_rate = 0
    else:
        acceptance_rate = (total_score/pr_number)

    response = {
        'acceptance_rate': acceptance_rate,
        'categories': categories
    }
    return response


def check_datetime(time_updated):
    '''
    verifies if the time difference between the pull request created and now
    is greater than X days
    '''

    time_updated = datetime.strptime(time_updated, '%Y-%m-%dT%H:%M:%SZ')
    last_updated = (datetime.now() - time_updated).days
    if last_updated <= LAST_UPDATED_TIME:
        return True
    else:
        return False
