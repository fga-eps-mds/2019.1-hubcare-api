import requests
import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from activity_rate.models import ActivityRateIssue
from activity_rate.serializers import ActivityRateIssueSerializer
# from issue_metrics.functions import calculate_metric, \
#         get_all_issues, check_datetime_15_days
from issue_metrics.constants import ISSUE_URL, TOTAL_DAYS
import os

from datetime import datetime, timezone, timedelta


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        Return activity rate to repo issues
        '''
        activity_rate = ActivityRateIssue.objects.get(
            owner=owner,
            repo=repo
        )
        activity_rate_serialized = ActivityRateIssueSerializer(
            activity_rate
        )

        return Response(
            activity_rate_serialized.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, owner, repo):
        '''
        Create new activity rate object
        '''

        data = ActivityRateIssue.objects.filter(
            owner=owner,
            repo=repo
        )
        # if data:
        #     serializer = ActivityRateIssueSerializer(data[0])
        #     return Response(serializer.data, status=status.HTTP_200_OK)

        interval = timedelta(days=TOTAL_DAYS)
        date = str(datetime.now() - interval).split(' ')[0]
        print('date = ', date)

        open_url = ISSUE_URL + '+repo:' + owner + '/' + repo
        open_issues = get_issues(open_url)

        active_url = open_url + '+created:<=' + date + '+updated:>=' + date
        active_issues = get_issues(active_url)

        new_url = open_url + '+created:>=' + date
        new_issues = get_issues(new_url)

        open_issues = open_issues['total_count']
        active_issues = active_issues['total_count']
        new_issues = new_issues['total_count']
        active_issues += new_issues

        metric = calculate_metric(open_issues, active_issues)
        return Response(metric)


def get_issues(url):
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    issues = requests.get(url, auth=(username,token)).json()
    return issues

def calculate_metric(open_issues, active_issues):
    print('open_issues = ', open_issues)
    print('active_issues = ', active_issues)
    if open_issues == 0:
        metric = 0
    else:
        metric = ((active_issues/open_issues)-0.5) * 4
        if metric > 1:
            metric = 1
        if metric < 0:
            metric = 0
    return metric
