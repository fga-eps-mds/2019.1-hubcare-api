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
        Input: owner, repo, token_auth
        Output: indicators
    '''
    def get(self, request, owner, repo, token_auth):
        '''
            Getting data from a repo and indicate parameters
            Input: owner, repo, token_auth
            Output: indicators
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        repo_request = requests.get(URL_REPOSITORY + owner + '/' + repo + '/' +
                                    token_auth + '/').json()
        response = []
        metrics = {}
        if repo_request['status'] == 0:
            return Response([response])
        elif repo_request['status'] == 1:
            print('###########INITIAL TIME POST############')
            now = datetime.now()
            print(now)
            print('###################################')

            metrics = get_metric(owner, repo, token_auth, 'post')
            hubcare_indicators = get_hubcare_indicators(owner, repo, token_auth,
                                                        metrics)
            response = create_response(
                metrics,
                hubcare_indicators,
                get_commit_graph(metrics),
                get_pull_request_graph(metrics)
            )

            repo_request = requests.post(
                URL_REPOSITORY + owner + '/' + repo + '/' + token_auth + '/'
            )

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ', (after-now))
            print('###################################')
            return Response([response])
        elif repo_request['status'] == 2:
            print('###########INITIAL TIME PUT############')
            now = datetime.now()
            print(now)
            print('#######################################')

            metrics = get_metric(owner, repo, token_auth, 'put')
            hubcare_indicators = get_hubcare_indicators(owner, repo, token_auth,
                                                        metrics)
            response = create_response(
                metrics,
                hubcare_indicators,
                get_commit_graph(metrics),
                get_pull_request_graph(metrics)
            )

            repo_request = requests.put(
                URL_REPOSITORY + owner + '/' + repo + '/' + token_auth + '/'
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

            metrics = get_metric(owner, repo, token_auth, 'get')
            hubcare_indicators = get_hubcare_indicators(owner, repo, token_auth,
                                                        metrics)

            response = create_response(
                metrics,
                hubcare_indicators,
                get_commit_graph(metrics),
                get_pull_request_graph(metrics)
            )

            print('############FINAL TIME#############')
            after = datetime.now()
            print(after)
            print('TOTAL = ', (after-now))
            print('###################################')

        return Response([metrics])


def create_response(metrics, indicators, commit_graph, pull_request_graph):
    graphs = {
        'commit_graph': commit_graph,
        'pull_request_graph': pull_request_graph
    }

    response = metrics
    response.update(indicators)
    response.update(graphs)
    return response


def get_metric(owner, repo, token_auth, request_type):
    metrics = issue_metric.get_metric(owner, repo, token_auth, request_type)
    metrics.update(community_metric.get_metric(owner, repo, token_auth, request_type))
    metrics.update(commit_metric.get_metric(owner, repo, token_auth, request_type))
    metrics.update(pull_request_metric.get_metric(owner, repo, token_auth,
                                                  request_type))

    return metrics


def get_hubcare_indicators(owner, repo, token_auth, metrics):
    active_data = active_indicator.get_active_indicator(owner, repo, token_auth, metrics)
    welcoming_data = welcoming_indicator.get_welcoming_indicator(
        owner,
        repo,
        metrics
    )
    support_data = support_indicator.get_support_indicator(owner, repo, token_auth,
                                                           metrics)
    hubcare_indicators = {
        'active_indicator': float(
            '{0:.2f}'.format(active_data*100)),
        'welcoming_indicator': float(
            '{0:.2f}'.format(welcoming_data*100)),
        'support_indicator': float(
            '{0:.2f}'.format(support_data*100)),
    }

    hubcare_indicators = {
        'indicators': hubcare_indicators
    }

    return hubcare_indicators


def get_pull_request_graph(metrics):
    metrics = metrics['pull_request_metric']
    categories = metrics['categories']
    x_axis = [
        'merged_yes',
        'merged_no',
        'open_yes_new',
        'closed_yes',
        'open_yes_old',
        'closed_no',
        'open_no_old'
    ]
    y_axis = []
    for i in x_axis:
        y_axis.append(categories[i])

    pull_request_graph_axis = {
        'x_axis': x_axis,
        'y_axis': y_axis
    }
    return pull_request_graph_axis


def get_commit_graph(metrics):
    metrics = metrics['commit_metric']
    commits_week = metrics['commits_week']
    commits_week = json.loads(commits_week)
    WEEKS = len(commits_week)
    if WEEKS == 0:
        x_axis = [str(TOTAL_WEEKS-i) + ' weeks ago'
                  for i in range(TOTAL_WEEKS-1)]
        x_axis.append('this week')
        y_axis = [0] * TOTAL_WEEKS
    else:
        x_axis = []
        y_axis = []

    for i in range(WEEKS-1):
        x_axis.append(str(WEEKS-i) + ' weeks ago')
        y_axis.append(commits_week[i])

    if WEEKS > 0:
        x_axis.append('this week')
        y_axis.append(commits_week[-1])
    commit_graph_axis = {
        'x_axis': x_axis,
        'y_axis': y_axis
    }
    return commit_graph_axis
