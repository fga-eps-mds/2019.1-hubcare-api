import requests
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PullRequestQuality
from .serializers import PullRequestQualitySerializers
from datetime import datetime, timezone


class PullRequestQualityView(APIView):
    def get(self, request, owner, repo):
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


def get_pull_request(owner, repo):
    '''
    Get all the pr's in the last 60 days or the first 50
    '''
    page_number = 1
    pull_request_score = 0
    elements = 0
    url = 'https://api.github.com/repos/' + owner + '/' + repo + \
          '/' + 'pulls?state=all&page='
    aux = True
    while aux:
        github_request = requests.get(url + str(page_number) + '&per_page=100')
        github_data = github_request.json()

        for pr in github_data:
            if(check_datetime_days(pr['created_at'], 60)):
                score = calculate_metric(owner, repo, pr)
                print("score = ", score)
                pull_request_score = pull_request_score + score
                print("pull_request_score =", pull_request_score)
                elements = elements + 1

            if(elements < 50):
                score = calculate_metric(owner, repo, pr)
                print("score = ", score)
                pull_request_score = pull_request_score + score
                print("pull_request_score =", pull_request_score)
                elements = elements + 1
            else:
                # Do nothing
                pass
        if(github_data == []):
            aux = False
        page_number = page_number + 1
    print("pull_request_score_total =", pull_request_score)
    pull_request_score = pull_request_score / elements
    print("elements =", elements)
    return pull_request_score


def calculate_metric(owner, repo, pr):
    '''
    Calculate metric

    Situação	Discussão	Resultado

    Merjado	Sim	1

    Merjado	Não	0.9

    Aberto	Recente (<=15 dias)	0.9

    Fechado e sem Merge	Sim	0.7

    Aberto	Antiga (>15 dias)	0.3

    Fechado e sem Merge	Não	0.1

    Aberto	Não / antiga	0
    '''
    comments = get_comments(owner, repo, pr['number'])

    if pr['merged_at'] is not None and comments >= 1:
        score = 1
        print("Merjado com Discussão")
    elif pr['merged_at'] is not None and comments == 0:
        score = 0.9
        print("Merjado sem Discussão")
    elif pr['state'] == 'open' and check_datetime_days(pr['updated_at'], 15):
        score = 0.9
        print("Aberto com Discussão Recente")
    elif pr['state'] == 'closed' and comments >= 1:
        print("Fechado com Discussão")
        score = 0.7
    elif pr['state'] == 'open' and not check_datetime_days(pr['updated_at'],
                                                           15):
        print("Aberto com Discussão Antiga")
        score = 0.3
    elif pr['state'] == 'closed' and comments == 0:
        print("Fechado sem Discussão")
        score = 0.1
    elif pr['state'] == 'open' and comments == 0:
        print("Aberto sem Discussão")
        score = 0
    return score


def get_comments(owner, repo, number):
    '''
    Get all the comments
    '''
    url = 'https://github.com/'
    github_page = requests.get(
        url + owner + '/' + repo + '/pull' + '/' + str(number))

    find = re.search(
        r'<span id="conversation_tab_counter" class="Counter">[^>]*>',
        github_page.text)

    if (find is None):
        return 0

    find_number = re.search(r'\d+', find[0])
    find_number = find_number[0].replace(',', '')

    comments = int(find_number)

    print("comments = ", comments)

    return comments
