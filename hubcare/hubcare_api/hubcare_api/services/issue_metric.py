from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, token_auth, request_type):

    r = Request()
    url_activity = get_url('activity_rate/', owner, repo, token_auth)
    url_help_wanted = get_url('help_wanted/', owner, repo, token_auth)
    url_good_first_issue = get_url('good_first_issue/', owner, repo,
                                   token_auth)

    if request_type == 'get':
        activity_rate = r.get(url_activity)
        help_wanted = r.get(url_help_wanted)
        good_first_issue = r.get(url_good_first_issue)
    elif request_type == 'post':
        activity_rate = r.post(url_activity)
        help_wanted = r.post(url_help_wanted)
        good_first_issue = r.post(url_good_first_issue)
    elif request_type == 'put':
        activity_rate = r.put(url_activity)
        help_wanted = r.put(url_help_wanted)
        good_first_issue = r.put(url_good_first_issue)

    metric = {
        'activity_rate': activity_rate['activity_rate'],
        'activity_max_rate': activity_rate['activity_max_rate'],
        'active_issues': activity_rate['active_issues'],
        'dead_issues': activity_rate['dead_issues'],
        'total_issues': help_wanted['total_issues'],
        'help_wanted_issues': help_wanted['help_wanted_issues'],
        'help_wanted_rate': help_wanted['help_wanted_rate'],
        'help_wanted_max_rate': help_wanted[
            'help_wanted_max_rate'],
        'good_first_issue': good_first_issue['good_first_issue'],
        'good_first_issue_rate': good_first_issue['good_first_issue_rate'],
        'good_first_issue_max_rate': good_first_issue[
            'good_first_issue_max_rate'],
    }

    issue_metric = {
        'issue_metric': metric
    }

    return issue_metric


def get_url(url_app, owner, repo, token_auth):
    return URL_ISSUE + url_app + owner + '/' + repo + '/' + token_auth + '/'
