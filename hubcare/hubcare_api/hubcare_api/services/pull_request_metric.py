from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_acceptance_quality = get_url('acceptance_quality/', owner, repo)

    if request_type == 'get':
        metric = {
            "acceptance_quality": r.get(url_acceptance_quality)[
                'acceptance_rate'
            ],
        }
    elif request_type == 'post':
        metric = {
            "acceptance_quality": r.post(url_acceptance_quality)[
                'acceptance_rate'
            ],
        }
    elif request_type == 'put':
        metric = {
            "acceptance_quality": r.put(url_acceptance_quality)[
                'acceptance_rate'
            ],
        }

    return metric


def get_url(url_app, owner, repo):
    return URL_PR + url_app + owner + '/' + repo + '/'
