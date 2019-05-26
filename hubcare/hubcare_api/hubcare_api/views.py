from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from hubcare_api.indicators import active_indicator
from hubcare_api.indicators import welcoming_indicator
from hubcare_api.indicators import support_indicator
from hubcare_api.services import issue_metric
from hubcare_api.services import community_metric
from hubcare_api.services import commit_metric
from hubcare_api.services import pull_request_metric
from hubcare_api.constants import URL_REPOSITORY, TOTAL_WEEKS
import requests
import json
import os


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
        metrics = {}
        if repo_request['status'] == 0:
            return Response(response)
        elif repo_request['status'] == 1:
            print('###########INITIAL TIME POST############')
            now = datetime.now()
            print(now)
            print('###################################')

            metrics = get_metric(owner, repo, 'post')
            hubcare_indicators = get_hubcare_indicators(owner, repo, metrics)
            commit_graph = {
                'commit_graph': get_commit_graph_axis(metrics)
            }
            response = hubcare_indicators
            response.update(commit_graph)
            repo_request = requests.post(
                URL_REPOSITORY + owner + '/' + repo + '/'
            )

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ', (after-now))
            print('###################################')
            return Response(response)
        elif repo_request['status'] == 2:
            print('###########INITIAL TIME PUT############')
            now = datetime.now()
            print(now)
            print('###################################')

            metrics = get_metric(owner, repo, 'put')
            hubcare_indicators = get_hubcare_indicators(owner, repo, metrics)
            commit_graph = {
                'commit_graph': get_commit_graph_axis(metrics)
            }
            response = hubcare_indicators
            response.update(commit_graph)
            repo_request = requests.put(
                URL_REPOSITORY + owner + '/' + repo + '/'
            )

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ', (after-now))
            print('###################################')
        elif repo_request['status'] == 3:
            print('###########INITIAL TIME GET############')
            now = datetime.now()
            print(now)
            print('###################################')

            metrics = get_metric(owner, repo, 'get')
            hubcare_indicators = get_hubcare_indicators(owner, repo, metrics)
            commit_graph = {
                'commit_graph': get_commit_graph_axis(metrics)
            }
            response = hubcare_indicators
            response.update(commit_graph)

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ', (after-now))
            print('###################################')

        return Response(response)


def get_metric(owner, repo, request_type):
    metrics = issue_metric.get_metric(owner, repo, request_type)
    metrics.update(community_metric.get_metric(owner, repo, request_type))
    metrics.update(commit_metric.get_metric(owner, repo, request_type))
    metrics.update(pull_request_metric.get_metric(owner, repo,
                                                  request_type))
    return metrics


def get_hubcare_indicators(owner, repo, metrics):
    active_data = active_indicator.get_active_indicator(owner, repo, metrics)
    welcoming_data = welcoming_indicator.get_welcoming_indicator(
        owner,
        repo,
        metrics
    )
    support_data = support_indicator.get_support_indicator(owner, repo,
                                                           metrics)
    hubcare_indicators = {
        'active_indicator': float(
            '{0:.2f}'.format(active_data*100)),
        'welcoming_indicator': float(
            '{0:.2f}'.format(welcoming_data*100)),
        'support_indicator': float(
            '{0:.2f}'.format(support_data*100)),
    }

    return hubcare_indicators


def get_commit_graph_axis(metrics):
    commits_week = metrics['commits_week']
    commits_week = json.loads(commits_week)
    WEEKS = len(commits_week)
    if WEEKS == 0:
        x_axis = ['Week ' + str(i+1) for i in range(TOTAL_WEEKS)]
        y_axis = [0] * TOTAL_WEEKS
    else:
        x_axis = []
        y_axis = []

    for i in range(WEEKS):
        x_axis.append('Week ' + str(i+1))
        y_axis.append(commits_week[i])
    commit_graph_axis = {
        'x_axis': x_axis,
        'y_axis': y_axis
    }
    return commit_graph_axis
