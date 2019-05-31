import requests
import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from acceptance_quality.models import PullRequestQuality
from acceptance_quality.serializers import PullRequestQualitySerializer
from datetime import datetime, timezone, timedelta
from pull_request_metrics.constants import TOTAL_DAYS, URL_PR, TOTAL_PR
import os


class PullRequestQualityView(APIView):
    def get(self, request, owner, repo):
        '''
        Returns the quality of the pull
        requests from the repository
        '''
        return Response('ok')
        quality = PullRequestQuality.objects.get(owner=owner, repo=repo)
        serializer = PullRequestQualitySerializer(quality)
        return Response(serializer.data)

    def post(self, request, owner, repo):
        '''
        Post a new quality of the pull
        requests from the repository
        '''


        print('############## INITIAL TIME ###############')
        time_now = datetime.now()
        print(time_now)
        print('###########################################')

        # return Response('ok')


        data = new_get_pull_request(owner, repo)
        # pr_quality = PullRequestQuality.objects.filter(
        #     owner=owner,
        #     repo=repo
        # )
        # if pr_quality:
        #     serializer = PullRequestQualitySerializer(pr_quality[0])
        #     return Response(serializer.data)

        # pr_quality = PullRequestQuality.objects.create(
        #     owner=owner,
        #     repo=repo,
        #     acceptance_rate=get_pull_request(owner, repo)
        # )
        pr_quality = PullRequestQuality()
        pr_quality.owner = owner
        pr_quality.repo = repo
        # pr_quality. acceptance_rate = get_pull_request(owner, repo)
        # serializer = PullRequestQualitySerializer(pr_quality)

        print('############## FINAL TIME ###############')
        time_after = datetime.now()
        print(time_after)
        print('TOTAL TIME = ', time_after - time_now)
        print('###########################################')

        return Response(data)

    def put(self, request, owner, repo):
        '''
        Update a quality of the pull requests
        from the repository
        '''
        pr_quality = PullRequestQuality.objects.get(owner=owner, repo=repo)
        pr_quality.acceptance_rate = get_pull_request(owner, repo)
        pr_quality.save()

        serializer = PullRequestQualitySerializer(pr_quality)
        return Response(serializer.data)


def check_datetime(pull_request):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - pull_request.date).days >= 1):
        return True
    return False


def check_datetime_days(pull_request, days):
    '''
    verifies if the time difference between the issue created and now is
    greater than X days
    '''
    pull_request = datetime.strptime(pull_request, '%Y-%m-%dT%H:%M:%SZ')
    datetime_now = datetime.now()
    if((datetime_now - pull_request).days <= days):
        return True
    return False


def new_get_pull_request(owner, repo):

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

    if updated_status != merged_status:
        return Response('Error on requesting GitHub API',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif updated_status >= 200 and updated_status < 300:
        updated = updated_request.json()['items']
        merged = merged_request.json()['items']
        new_get_metric(updated, merged)
    else:
        return Response('Error on requesting GitHub API',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return updated

def new_get_metric(updated, merged):
    '''
    Calculate pull request quality metric

    Situation	Discussion	Result

    Merged      Yes	        1

    Merged	    No	        0.9

    Open    Recent (<=15 days)	0.9

    Closed and without merged	Yes     0.7

    Open	Old (>15 days)	0.3

    Closed and without merged	No	0.1

    Open        No/old      0
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
            if new_check_datetime(i['updated_at']):
                total_score += 0.9
                categories['open_yes_new'] += 1
            else:
                total_score += 0.3
                categories['open_yes_old'] += 1
        else:
            categories['open_no_old'] += 1
        pr_number += 1
    print ('total_score =', total_score/pr_number)

def new_check_datetime(time_updated):
    time_updated = datetime.strptime(time_updated, '%Y-%m-%dT%H:%M:%SZ')
    last_updated = (datetime.now() - time_updated).days
    print('last_updated = ', last_updated)
    if last_updated <= 15:
        return True
    else:
        return False

def check_category(owner, repo, number):

    url = 'https://api.github.com/repos/'
    github_request = requests.get(
        url + owner + '/' + repo + '/pulls' + '/' + str(number),
        auth=(username, token)
    )
    if github_request.status_code == 404:
        print('########### DEU RUIM ###########')

def get_pull_request(owner, repo):
    '''
    Get all the pr's in the last 60 days or the first 50
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']
    page_number = 1
    pull_request_score = 0
    elements = 0
    url = 'https://api.github.com/repos/{0}/{1}/pulls?state=all&page='.format(
        owner,
        repo
    )
    aux = True
    while aux:
        github_request = requests.get(url + str(page_number) + '&per_page=100',
                                      auth=(username, token))
        github_data = github_request.json()

        if (github_data == [] and elements == 0):
            return 0

        for pr in github_data:
            if(check_datetime_days(pr['created_at'], 60) and elements < 50):
                score = calculate_metric(owner, repo, pr)
                print("score = ", score)
                pull_request_score = pull_request_score + score
                print("pull_request_score =", pull_request_score)
                elements = elements + 1
            elif(elements < 50):
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
        if(elements == 50):
            aux = False
        page_number = page_number + 1
    print("pull_request_score_total =", pull_request_score)
    pull_request_score = pull_request_score / elements
    print("elements =", elements)
    return pull_request_score


def calculate_metric(owner, repo, pr):
    '''
    Calculate pull request quality metric

    Situation	Discussion	Result

    Merged      Yes	        1

    Merged	    No	        0.9

    Open    Recent (<=15 days)	0.9

    Closed and without merged	Yes     0.7

    Open	Old (>15 days)	0.3

    Closed and without merged	No	0.1

    Open        No/old      0
    '''
    comments = get_comments(owner, repo, pr['number'])

    if pr['merged_at'] is not None and comments >= 1:
        score = 1
        print("Merged with discussion")
    elif pr['merged_at'] is not None and comments == 0:
        score = 0.9
        print("Merged without discussion")
    elif pr['state'] == 'open' and check_datetime_days(pr['updated_at'], 15):
        score = 0.9
        print("Open with discussion recent")
    elif pr['state'] == 'closed' and comments >= 1:
        print("Closed with discussion")
        score = 0.7
    elif pr['state'] == 'open' and not check_datetime_days(pr['updated_at'],
                                                           15):
        print("Open without discussion")
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
    if github_request.status_code == 404:
        print('########### DEU RUIM ###########')
    github_data = github_request.json()

    comments = github_data['comments'] + github_data['review_comments']
    print("comments = ", comments)

    return comments
