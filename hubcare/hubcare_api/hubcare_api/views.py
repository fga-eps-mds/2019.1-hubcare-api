from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from hubcare_api.indicators import active_indicator
from hubcare_api.indicators import welcoming_indicator
from hubcare_api.indicators import support_indicator
import requests
import os
from hubcare_api.constants import URL_REPOSITORY

from hubcare_api.services import issue_metric
from hubcare_api.services import community_metric
from hubcare_api.services import commit_metric
from hubcare_api.services import pull_request_metric

from datetime import datetime, timezone


class HubcareApiView(APIView):
    '''
        This is the main class view of the project, it gets data from a repo
        Input: owner, repo
        Output: indicators
    '''
    def get(self, request, owner, repo):
        '''
            Getting data from a repo and indicate parameters
            Input: owner, repo
            Output: indicators
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']


        repo_request = requests.get(URL_REPOSITORY + owner + '/' + repo).json()
        response = []
        if repo_request['status'] == 0:
            return Response(response)
        elif repo_request['status'] == 1:
            print('###########INITIAL TIME POST############')
            now = datetime.now()
            print(now)
            print('###################################')


            response.append(issue_metric.get_metric(owner, repo, 'post'))
            response.append(community_metric.get_metric(owner, repo, 'post'))
            response.append(commit_metric.get_metric(owner, repo, 'post'))
            response.append(pull_request_metric.get_metric(owner, repo, 'post'))


            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ',(after-now))
            print('###################################')
            return Response(response)
        elif repo_request['status'] == 2:
            print('###########INITIAL TIME PUT############')
            now = datetime.now()
            print(now)
            print('###################################')


            response.append(issue_metric.get_metric(owner, repo, 'put'))
            response.append(community_metric.get_metric(owner, repo, 'put'))
            response.append(commit_metric.get_metric(owner, repo, 'put'))
            response.append(pull_request_metric.get_metric(owner, repo, 'put'))
            

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ',(after-now))
            print('###################################')
        elif repo_request['status'] == 3:
            print('###########INITIAL TIME GET############')
            now = datetime.now()
            print(now)
            print('###################################')


            response.append(issue_metric.get_metric(owner, repo, 'get'))
            response.append(community_metric.get_metric(owner, repo, 'get'))
            response.append(commit_metric.get_metric(owner, repo, 'get'))
            response.append(pull_request_metric.get_metric(owner, repo, 'get'))
            

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ',(after-now))
            print('###################################')

        return Response(response)




        # url = 'https://api.github.com/repos/'
        # github_request = requests.get(url + owner + '/' + repo,
        #                               auth=(username, token))

        # if github_request.status_code == 200:
        #     active_data = active_indicator.get_active_indicator(owner, repo)
        #     welcoming_data = welcoming_indicator.get_welcoming_indicator(
        #         owner,
        #         repo
        #     )
        #     support_data = support_indicator.get_support_indicator(owner, repo)
        #     hubcare_indicators = [
        #         {
        #             "active_indicator": float(
        #                 "{0:.2f}".format(active_data*100)),
        #             "welcoming_indicator": float(
        #                 "{0:.2f}".format(welcoming_data*100)),
        #             "support_indicator": float(
        #                 "{0:.2f}".format(support_data*100)),
        #         }
        #     ]

        #     return Response(hubcare_indicators)
        # else:
        #     raise Http404
