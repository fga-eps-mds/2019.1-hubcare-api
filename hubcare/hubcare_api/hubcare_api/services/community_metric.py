from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, token_auth, request_type):

    r = Request()
    url_code_of_conduct = get_url('code_of_conduct/', owner, repo, token_auth)
    url_contribution_guide = get_url('contribution_guide/', owner, repo,
                                     token_auth)
    url_issue_template = get_url('issue_template/', owner, repo, token_auth)
    url_license = get_url('license/', owner, repo, token_auth)
    url_pull_request_template = get_url('pull_request_template/', owner, repo,
                                        token_auth)
    url_release_note = get_url('release_note/', owner, repo, token_auth)
    url_readme = get_url('readme/', owner, repo, token_auth)
    url_description = get_url('description/', owner, repo, token_auth)

    if request_type == 'get':
        metric = {
            "code_of_conduct": r.get(url_code_of_conduct)['code_of_conduct'],
            "contribution_guide": r.get(url_contribution_guide)[
                'contribution_guide'
            ],
            "issue_template": r.get(url_issue_template)['issue_template'],
            "license": r.get(url_license)['license'],
            "pull_request_template": r.get(url_pull_request_template)[
                'pull_request_template'
            ],
            "release_note": r.get(url_release_note)['release_note'],
            "readme": r.get(url_readme)['readme'],
            "description": r.get(url_description)['description'],
        }
    elif request_type == 'post':
        metric = {
            "code_of_conduct": r.post(url_code_of_conduct)['code_of_conduct'],
            "contribution_guide": r.post(url_contribution_guide)[
                'contribution_guide'
            ],
            "issue_template": r.post(url_issue_template)['issue_template'],
            "license": r.post(url_license)['license'],
            "pull_request_template": r.post(url_pull_request_template)[
                'pull_request_template'
            ],
            "release_note": r.post(url_release_note)['release_note'],
            "readme": r.post(url_readme)['readme'],
            "description": r.post(url_description)['description'],
        }
    elif request_type == 'put':
        metric = {
            "code_of_conduct": r.put(url_code_of_conduct)['code_of_conduct'],
            "contribution_guide": r.put(url_contribution_guide)[
                'contribution_guide'
            ],
            "issue_template": r.put(url_issue_template)['issue_template'],
            "license": r.put(url_license)['license'],
            "pull_request_template": r.put(url_pull_request_template)[
                'pull_request_template'
            ],
            "release_note": r.put(url_release_note)['release_note'],
            "readme": r.put(url_readme)['readme'],
            "description": r.put(url_description)['description'],
        }

    community_metric = {
        'community_metric': metric
    }

    return community_metric


def get_url(url_app, owner, repo, token_auth):
    return (URL_COMMUNITY + url_app + owner + '/' + repo + '/' +
            token_auth + '/')
