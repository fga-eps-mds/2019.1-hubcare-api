from datetime import datetime, timezone
from issue_metrics.constants import main_url, ZERO
from rest_framework.response import Response
import json
import requests
import os
import re


def check_datetime(object_date):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - object_date.date_time).days >= 1):
        return True
    return False


def get_metric_good_first_issue(ObjectMetric, owner, repo):
    '''
    returns the metric of the repository
    '''
    object_metric = ObjectMetric.objects.all().filter(
        owner=owner,
        repo=repo
    )[0]
    if object_metric.total_issues != 0:
        total_sample = object_metric.total_issues
        rate = object_metric.good_first_issue / total_sample
    else:
        rate = 0.0
    rate = '{"rate":\"' + str(rate) + '"}'
    rate_json = json.loads(rate)
    return rate_json


def count_all_label(url, result):
    '''
    returns the number of good first issue in all pages
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    count = 1
    page = '&page='
    labels = ZERO
    while result:
        count += 1
        labels += len(result)
        result = requests.get(url + page + str(count),
                              auth=(username, token)).json()

        return labels


def get_metric_help_wanted(ObjectMetric, owner, repo):
    '''
    returns the metric of the repository
    '''
    help_wanted = ObjectMetric.objects.all().filter(
        owner=owner,
        repo=repo
    )[0]
    if help_wanted.total_issues != 0:
        rate = help_wanted.help_wanted_issues / help_wanted.total_issues
    else:
        rate = 0.0
    rate = '{"rate":\"' + str(rate) + '"}'
    rate_json = json.loads(rate)
    return rate_json


def calculate_metric(issues_alive, open_issues):
    '''
    Calculate metrics for activity rate
    '''
    if(open_issues != 0):
        metric = ((issues_alive / open_issues) - 0.5) * 4
    else:
        metric = 0

    if metric > 1:
        metric = 1
    elif metric < 0:
        metric = 0

    return metric


def get_all_issues(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    github_page = requests.get(
        'https://github.com/' + owner + '/' + repo + '/issues')
    find = re.search(r'(.*) Open\n', github_page.text)
    if (find is None):
        return 0, 0
    open_issues = int(find.group(1).replace(',', ''))

    find = re.search(r'(.*) Closed\n', github_page.text)
    closed_issues = int(find.group(1).replace(',', ''))

    return open_issues, closed_issues


def check_datetime_15_days(activity_rate):
    '''
    verifies if the time difference between the issue created and now is
    greater than 15 days
    '''
    activity_rate = datetime.strptime(activity_rate, '%Y-%m-%dT%H:%M:%SZ')
    datetime_now = datetime.now()
    if((datetime_now - activity_rate).days <= 15):
        return True
    return False
