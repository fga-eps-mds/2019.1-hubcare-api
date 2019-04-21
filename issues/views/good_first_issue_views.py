from rest_framework.views import APIView
from rest_framework.response import Response
from issues.models.good_first_issue_model import GoodFirstIssue
from issues.serializers.good_first_issue_serializer \
    import GoodFirstIssueSerializer
from datetime import datetime, timezone
import requests
import json
from issues import constants


class GoodFirstIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        returns good first issue rate
        '''
        good_first_issues = GoodFirstIssue.objects.all().filter(
            owner=owner,
            repo=repo
        )
        url = constants.main_url + owner + '/' + repo
        if(not good_first_issues):
            total_issues, good_first_issue = self.get_total_goodfirstissue(url)
            GoodFirstIssue.objects.create(
                owner=owner,
                repo=repo,
                total_issues=total_issues,
                good_first_issue=good_first_issue,
                date_time=datetime.now(
                    timezone.ut
                )
            )
        elif check_datetime(good_first_issues[0]):
            good_first_issues = GoodFirstIssue.objects.get(
                owner=owner,
                repo=repo
            )
            total_issues, good_first_issue = self.get_total_goodfirstissue(url)
            GoodFirstIssue.objects.filter(owner=owner, repo=repo).update(
                total_issues=total_issues,
                good_first_issue=good_first_issue,
                date_time=datetime.now(
                    timezone.utc
                )
            )
        return Response(self.get_metric(owner, repo))

    def get_total_goodfirstissue(self, url):
        '''
        returns the number of all issues and the issues with
        good first issue label
        '''
        total_issues = 0
        good_first_issue = 0
        info_repo = requests.get(url).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.label_good_first_issue_spaces
        result = requests.get(label_url + page).json()

        '''
        checks possibilities for different aliases of good first issue
        '''
        if result:
            good_first_issue = self.count_all_goodfirstissue(label_url, result)
        else:
            label_url = url + constants.label_goodfirstissue
            result = requests.get(label_url + page).json()
            if result:
                good_first_issue = self.count_all_goodfirstissue(
                    label_url,
                    result
                )
            else:
                label_url = url + constants.label_good_first_issue
                result = requests.get(label_url + page).json()
                if result:
                    good_first_issue = self.count_all_goodfirstissue(
                        label_url,
                        result
                    )
        return total_issues, good_first_issue

    def count_all_goodfirstissue(self, url, result):
        '''
        returns the number of good first issue in all pages
        '''
        count = 1
        page = '&page='
        good_first_issue = 0
        while result:
            count += 1
            good_first_issue += len(result)
            result = requests.get(url + page + str(count)).json()
        return good_first_issue

    def get_metric(self, owner, repo):
        '''
        returns the metric of the repository
        '''
        good_first_issues = GoodFirstIssue.objects.all().filter(
            owner=owner,
            repo=repo
        )[0]
        if good_first_issues.total_issues != 0:
            total_sample = good_first_issues.total_issues
            rate = good_first_issues.good_first_issue / total_sample
        else:
            rate = 0.0
        rate = '{"rate":\"' + str(rate) + '"}'
        rate_json = json.loads(rate)
        return rate_json


def check_datetime(good_first_issue):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - good_first_issue.date_time).days >= 1):
        return True
    return False
