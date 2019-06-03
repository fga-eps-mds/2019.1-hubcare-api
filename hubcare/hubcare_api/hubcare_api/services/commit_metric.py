from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_commit_month = get_url('commit_month/', owner, repo)
    url_contributors = get_url('contributors/', owner, repo)

    if request_type == 'get':
        metric = {
            "total_commits": r.get(url_commit_month)['total_commits'],
            "commits_week": r.get(url_commit_month)['commits_week'],
            "differents_authors": r.get(url_contributors)
            ['differents_authors'],
        }
    elif request_type == 'post':
        metric = {
            "total_commits": r.post(url_commit_month)['total_commits'],
            "commits_week": r.post(url_commit_month)['commits_week'],
            "differents_authors": r.post(url_contributors)
            ['differents_authors'],
        }
    elif request_type == 'put':
        metric = {
            "total_commits": r.put(url_commit_month)['total_commits'],
            "commits_week": r.put(url_commit_month)['commits_week'],
            "differents_authors": r.put(url_contributors)
            ['differents_authors'],
        }
    return metric


def get_url(url_app, owner, repo):
    return URL_COMMIT + url_app + owner + '/' + repo + '/'
