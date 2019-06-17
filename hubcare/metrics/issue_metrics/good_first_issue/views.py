from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from good_first_issue.models import GoodFirstIssue
from good_first_issue.serializers import GoodFirstIssueSerializer
from issue_metrics.functions import count_all_label
from issue_metrics import constants
import requests
import json
import os

from datetime import datetime, timezone


class GoodFirstIssueView(APIView):
    def get(self, request, owner, repo, token_auth):
        '''
        Returns good first issue data
        '''

        good_first_issue = GoodFirstIssue.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = GoodFirstIssueSerializer(good_first_issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo, token_auth):
        '''
        Creates good first issue data for repository
        '''
        data = GoodFirstIssue.objects.filter(
            owner=owner,
            repo=repo
        )
        if data:
            serializer = GoodFirstIssueSerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, good_first_issue = self.get_total_goodfirstissue(
                                         url, token_auth)
        if total_issues == 0:
            rate = 0
        else:
            rate = good_first_issue/total_issues
        data = GoodFirstIssue.objects.create(
            owner=owner,
            repo=repo,
            total_issues=total_issues,
            good_first_issue=good_first_issue,
            good_first_issue_max_rate=constants.GOOD_FIRST_ISSUE_MAX_RATE,
            good_first_issue_rate=rate
        )

        serializer = GoodFirstIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo, token_auth):
        '''
        Updates good first issue data for repository
        '''

        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, good_first_issue = self.get_total_goodfirstissue(
                                         url, token_auth)
        if total_issues == 0:
            rate = 0
        else:
            rate = good_first_issue/total_issues
        data = GoodFirstIssue.objects.get(
            owner=owner,
            repo=repo
        )
        data.total_issues = total_issues
        data.good_first_issue = good_first_issue
        data.good_first_issue_rate = rate
        data.good_first_issue_max_rate = constants.GOOD_FIRST_ISSUE_MAX_RATE
        data.save()

        serializer = GoodFirstIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_total_goodfirstissue(self, url, token_auth):
        '''
        returns the number of all issues and the issues with
        good first issue label
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        total_issues = 0
        good_first_issue = 0
        info_repo = requests.get(url, headers={'Authorization': 'token ' +
                                               token_auth}).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.LABEL_GOOD_FIRST_ISSUE_SPACES
        result = requests.get(label_url + page,
                              headers={'Authorization': 'token ' +
                                       token_auth}).json()

        '''
        checks possibilities for different aliases of good first issue
        '''
        if result:
            good_first_issue = count_all_label(
                label_url,
                result,
                token_auth
            )
        else:
            label_url = url + constants.LABEL_GOODFIRSTISSUE
            result = requests.get(label_url + page,
                                  headers={'Authorization': 'token ' +
                                           token_auth}).json()
            if result:
                good_first_issue = count_all_label(
                    label_url,
                    result,
                    token_auth
                )
            else:
                label_url = url + constants.LABEL_GOOD_FIRST_ISSUE
                result = requests.get(label_url + page,
                                      headers={'Authorization': 'token ' +
                                               token_auth}).json()
                if result:
                    good_first_issue = count_all_label(
                        label_url,
                        result,
                        token_auth
                    )
        return total_issues, good_first_issue
