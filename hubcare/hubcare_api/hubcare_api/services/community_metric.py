from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_code_of_conduct = get_url('code_of_conduct/', owner, repo)
    url_contribution_guide = get_url('contribution_guide/', owner, repo)
    url_issue_template = get_url('issue_template/', owner, repo)
    url_license = get_url('license/', owner, repo)
    url_pull_request_template = get_url('pull_request_template/', owner, repo)
    url_release_note = get_url('release_note/', owner, repo)
    url_readme = get_url('readme/', owner, repo)
    url_description = get_url('description/', owner, repo)

    metric = []
    if request_type == 'get':
        metric.append(r.get(url_code_of_conduct))
        metric.append(r.get(url_contribution_guide))
        metric.append(r.get(url_issue_template))
        metric.append(r.get(url_license))
        metric.append(r.get(url_pull_request_template))
        metric.append(r.get(url_release_note))
        metric.append(r.get(url_readme))
        metric.append(r.get(url_description))
    elif request_type == 'post':
        metric.append(r.post(url_code_of_conduct))
        metric.append(r.post(url_contribution_guide))
        metric.append(r.post(url_issue_template))
        metric.append(r.post(url_license))
        metric.append(r.post(url_pull_request_template))
        metric.append(r.post(url_release_note))
        metric.append(r.post(url_readme))
        metric.append(r.post(url_description))
    elif request_type == 'put':
        metric.append(r.put(url_code_of_conduct))
        metric.append(r.put(url_contribution_guide))
        metric.append(r.put(url_issue_template))
        metric.append(r.put(url_license))
        metric.append(r.put(url_pull_request_template))
        metric.append(r.put(url_release_note))
        metric.append(r.put(url_readme))
        metric.append(r.put(url_description))

    return metric


def get_url(url_app, owner, repo):
    return URL_COMMUNITY + url_app + owner + '/' + repo + '/'
