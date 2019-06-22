from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, token_auth, request_type):

    r = Request()
    url_commit_month = get_url('commit_month/', owner, repo, token_auth)
    url_contributors = get_url('contributors/', owner, repo, token_auth)

    if request_type == 'get':
        response = r.get(url_commit_month)
        metric = {
            'total_commits': response['total_commits'],
            'commits_last_period': response['commits_last_period'],
            'commits_week': response['commits_week'],
            'commits_high_score': response['commits_high_score'],
            "differents_authors": r.get(url_contributors)
            ['differents_authors'],
        }
    elif request_type == 'post':
        response = r.post(url_commit_month)
        metric = {
            'total_commits': response['total_commits'],
            'commits_last_period': response['commits_last_period'],
            'commits_week': response['commits_week'],
            'commits_high_score': response['commits_high_score'],
            "differents_authors": r.post(url_contributors)
            ['differents_authors'],
        }
    elif request_type == 'put':
        response = r.put(url_commit_month)
        metric = {
            'total_commits': response['total_commits'],
            'commits_last_period': response['commits_last_period'],
            'commits_week': response['commits_week'],
            'commits_high_score': response['commits_high_score'],
            "differents_authors": r.put(url_contributors)
            ['differents_authors'],
        }

    commit_metric = {
        'commit_metric': metric
    }

    return commit_metric


def get_url(url_app, owner, repo, token_auth):
    return URL_COMMIT + url_app + owner + '/' + repo + '/' + token_auth + '/'
