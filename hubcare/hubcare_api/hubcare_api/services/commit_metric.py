from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_commit_month = get_url('commit_month/', owner, repo)

    if request_type == 'get':
        response = r.get(url_commit_month)
        metric = {
            "total_commits": response['total_commits'],
            "commits_week": response['commits_week'],
        }
    elif request_type == 'post':
        response = r.post(url_commit_month)
        metric = {
            "total_commits": response['total_commits'],
            "commits_week": response['commits_week'],
        }
    elif request_type == 'put':
        response = r.put(url_commit_month)
        metric = {
            "total_commits": response['total_commits'],
            "commits_week": response['commits_week'],
        }

    return metric


def get_url(url_app, owner, repo):
    return URL_COMMIT + url_app + owner + '/' + repo + '/'
