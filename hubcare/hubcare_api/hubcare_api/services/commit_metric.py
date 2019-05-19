from hubcare_api.constants import *
from hubcare_api.services.request import Request

def get_metric(owner, repo, request_type):

    r = Request()
    url_commit_month = get_url('commit_month/', owner, repo)

    metric = []
    if request_type == 'get':
        metric.append(r.get(url_commit_month))
    elif request_type == 'post':
        metric.append(r.post(url_commit_month))
    elif request_type == 'put':
        metric.append(r.put(url_commit_month))
        
    return metric

def get_url(url_app, owner, repo):
    return URL_COMMIT + url_app + owner + '/' + repo + '/'