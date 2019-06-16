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
    count = 1
    page = '&page='
    labels = 0
    while result:
        count += 1
        labels += len(result)
        result = requests.get(url + page + str(count),
                              headers={'Authorization': 'token ' +
                              token_auth}).json()

    return labels
