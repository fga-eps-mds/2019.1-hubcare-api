import requests
import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from activity_rate.models import ActivityRateIssue
from activity_rate.serializers import ActivityRateIssueSerializer
# from issue_metrics.functions import calculate_metric, \
#         get_all_issues, check_datetime_15_days
from issue_metrics.constants import ISSUE_URL, TOTAL_DAYS, ACTIVITY_MAX_RATE
import os

from datetime import datetime, timezone, timedelta


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo, token_auth):
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

    def post(self, request, owner, repo, token_auth):
        '''
        Creates new activity rate object
        '''

        activity_object = ActivityRateIssue.objects.filter(
            owner=owner,
            repo=repo
        )
        if activity_object:
            serializer = ActivityRateIssueSerializer(activity_object[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        open_issues, active_issues = get_number_issues(owner, repo, token_auth)
        metric = calculate_metric(open_issues, active_issues)
        dead_issues = open_issues - active_issues

        activity_object = ActivityRateIssue.objects.create(
            owner=owner,
            repo=repo,
            activity_rate=metric,
            activity_max_rate=ACTIVITY_MAX_RATE,
            active_issues=active_issues,
            dead_issues=dead_issues
        )

        serializer = ActivityRateIssueSerializer(activity_object)
        return Response(serializer.data)

    def put(self, request, owner, repo, token_auth):
        '''
        Updates activity rate object
        '''

        activity_object = ActivityRateIssue.objects.get(
            owner=owner,
            repo=repo
        )

        open_issues, active_issues = get_number_issues(owner, repo, token_auth)
        metric = calculate_metric(open_issues, active_issues)
        dead_issues = open_issues - active_issues

        activity_object.activity_rate = metric
        activity_object.max_rate = ACTIVITY_MAX_RATE
        activity_object.active_issues = active_issues
        activity_object.dead_issues = dead_issues
        activity_object.save()

        serializer = ActivityRateIssueSerializer(activity_object)
        return Response(serializer.data)


def get_number_issues(owner, repo, token_auth):
    interval = timedelta(days=TOTAL_DAYS)
    date = str(datetime.now() - interval).split(' ')[0]

    open_url = ISSUE_URL + '+repo:' + owner + '/' + repo
    open_issues = request_issues(open_url, token_auth)

    active_url = open_url + '+created:<=' + date + '+updated:>=' + date
    active_issues = request_issues(active_url, token_auth)

    new_url = open_url + '+created:>=' + date
    new_issues = request_issues(new_url, token_auth)

    open_issues = open_issues['total_count']
    active_issues = active_issues['total_count']
    new_issues = new_issues['total_count']

    active_issues += new_issues

    return open_issues, active_issues


def request_issues(url, token_auth):
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    issues = requests.get(url, headers={'Authorization': 'token ' +
                          token_auth}).json()
    return issues


def calculate_metric(open_issues, active_issues):
    if open_issues == 0:
        metric = 0
    else:
        metric = ((active_issues/open_issues)-0.5) * 4
        if metric > 1:
            metric = 1
        if metric < 0:
            metric = 0
    return metric
