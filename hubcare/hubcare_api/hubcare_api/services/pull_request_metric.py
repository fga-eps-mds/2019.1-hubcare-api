from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, token_auth, request_type):

    r = Request()
    url_acceptance_quality = get_url('acceptance_quality/', owner, repo,
                                     token_auth)

    if request_type == 'get':
        metric = r.get(url_acceptance_quality)
    elif request_type == 'post':
        metric = r.post(url_acceptance_quality)
    elif request_type == 'put':
        metric = r.put(url_acceptance_quality)

    pull_request_metric = {
        'pull_request_metric': metric
    }

    return pull_request_metric


def get_url(url_app, owner, repo, token_auth):
    return URL_PR + url_app + owner + '/' + repo + '/' + token_auth + '/'
