from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_acceptance_quality = get_url('acceptance_quality/', owner, repo)

    metric = []
    if request_type == 'get':
        metric.append(r.get(url_acceptance_quality))
    elif request_type == 'post':
        metric.append(r.post(url_acceptance_quality))
    elif request_type == 'put':
        metric.append(r.put(url_acceptance_quality))

    return metric


def get_url(url_app, owner, repo):
    return URL_PR + url_app + owner + '/' + repo + '/'
