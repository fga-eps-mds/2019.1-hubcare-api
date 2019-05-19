from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from good_first_issue.models import GoodFirstIssue
from good_first_issue.serializers import GoodFirstIssueSerializer
from issue_metrics import constants
from issue_metrics.functions \
    import get_metric_good_first_issue, count_all_label
import requests
import json
import os

from datetime import datetime, timezone


class GoodFirstIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        Returns good first issue data
        '''

        try:
            good_first_issue = GoodFirstIssue.objects.all().filter(
                owner=owner,
                repo=repo
            )[0]
            serializer = GoodFirstIssueSerializer(good_first_issue)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepositoryNotFound:
            return Response('There is no repository to be viewed',
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, owner, repo):
        '''
        Creates good first issue data for repository
        '''

        print('time good_first_issue 1', datetime.now())
        url = constants.MAIN_URL + owner + '/' + repo
        total_issues, good_first_issue = self.get_total_goodfirstissue(url)
        data = {
            'owner': owner,
            'repo': repo,
            'total_issues': total_issues,
            'good_first_issue:': good_first_issue
        }

        serializer = GoodFirstIssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('time good_first_issue 2', datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Error on creating good first issue metric',
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner, repo):
        '''
        Updates good first issue data for repository
        '''

        good_first_issue_object = GoodFirstIssue.objects.filter(
            owner=owner,
            repo=repo
        )[0]

        url = constants.MAIN_URL + owner + '/' + repo
        total_issues, good_first_issue = self.get_total_goodfirstissue(url)
        data = {
            'total_issues': total_issues,
            'good_first_issue': good_first_issue
        }

        serializer = GoodFirstIssueSerializer(good_first_issue_object, data,
                                              partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Error on updating good first issue metric',
                            status=status.HTTP_400_BAD_REQUEST)

    def get_total_goodfirstissue(self, url):
        '''
        returns the number of all issues and the issues with
        good first issue label
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        total_issues = constants.ZERO
        good_first_issue = constants.ZERO
        info_repo = requests.get(url, auth=(username,
                                            token)).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.LABEL_GOOD_FIRST_ISSUE_SPACES
        result = requests.get(label_url + page,
                              auth=(username,
                                    token)).json()

        '''
        checks possibilities for different aliases of good first issue
        '''
        if result:
            good_first_issue = count_all_label(
                label_url,
                result
            )
        else:
            label_url = url + constants.LABEL_GOODFIRSTISSUE
            result = requests.get(label_url + page,
                                  auth=(username,
                                        token)).json()
            if result:
                good_first_issue = count_all_label(
                    label_url,
                    result
                )
            else:
                label_url = url + constants.LABEL_GOOD_FIRST_ISSUE
                result = requests.get(label_url + page,
                                      auth=(username,
                                            token)).json()
                if result:
                    good_first_issue = count_all_label(
                        label_url,
                        result
                    )
        return total_issues, good_first_issue
