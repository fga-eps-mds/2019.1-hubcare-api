from datetime import datetime, timezone
from issue_metrics.constants \
    import MAIN_URL, FIFTEEN_DAYS
from rest_framework.response import Response
import json
import requests
import os
import re


def count_all_label(url, result):
    '''
    returns the number of good first issue in all pages
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    count = ONE
    page = '&page='
    labels = ZERO
    while result:
        count += ONE
        labels += len(result)
        result = requests.get(url + page + str(count),
                              auth=(username, token)).json()

        return labels


def calculate_metric(issues_alive, open_issues):
    '''
    Calculate metrics for activity rate
    '''
    if(open_issues != ZERO):
        metric = ((issues_alive / open_issues) - 0.5) * 4
    else:
        metric = ZERO

    if metric > ONE:
        metric = ONE
    elif metric < ZERO:
        metric = ZERO

    return metric


def get_all_issues(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    github_page = requests.get(
        'https://github.com/' + owner + '/' + repo + '/issues')
    find = re.search(r'(.*) Open\n', github_page.text)
    if (find is None):
        return ZERO, ZERO
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
    if((datetime_now - activity_rate).days <= FIFTEEN_DAYS):
        return True
    return False
