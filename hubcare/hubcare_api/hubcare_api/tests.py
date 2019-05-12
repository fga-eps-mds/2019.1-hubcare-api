from django.test import RequestFactory, TestCase
from unittest import mock
from datetime import datetime
from commit_week.views import CommitMonthView
from hubcare.hubcare_api.hubcare_api.indicators.active_indicator import get_active_indicator
from hubcare.hubcare_api.hubcare_api.indicators.support_indicator import get_support_indicator
from hubcare.hubcare_api.hubcare_api.indicators.welcoming_indicator import get_welcoming_indicator
from hubcare.hubcare_api.hubcare_api.views import HubcareApiView
from hubcare.hubcare_api.hubcare_api.constants import *


def mocked_requests_get(*args, **kwargs):
    '''
    This method will be used by the mock to replace requests.get
    '''
    class MockResponse:
        '''
        define response to mock request
        '''
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            '''
            return all datas in object
            '''
            return self.json_data

    if args[0] == URL_COMMUNITY + 'code_of_conduct/test/repo_test':
        return MockResponse({'code_of_conduct':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'contribution_guide/test/repo_test':
        return MockResponse({'contribution_guide':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'description/test/repo_test':
        return MockResponse({'description':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'issue_template/test/repo_test':
        return MockResponse({'issue_templates':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'license/test/repo_test':
        return MockResponse({'have_license':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'pull_request_template/test/repo_test':
        return MockResponse({'pull_request_template':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'readme/test/repo_test':
        return MockResponse({'readme':'value'}, 200)
    elif args[0] == URL_COMMUNITY + 'release_note/test/repo_test':
        return MockResponse({'response':'value'}, 200)
    elif args[0] == URL_COMMIT + 'commit_week/commit_week/test/repo_test':
        return MockResponse({'sum':'273'}, 200)
    elif args[0] == URL_COMMIT + 'contributors/different_authors/test/repo_test':
        return MockResponse({'sum':'value'}, 200)
    elif args[0] == URL_ISSUE + 'activity_rate/test/repo_test':
        return MockResponse({'activity_rate_15_days':'1'}, 200)
    elif args[0] == URL_ISSUE + 'good_first_issue/test/repo_test':
        return MockResponse({'rate':'0.8'}, 200)
    elif args[0] == URL_ISSUE + 'help_wanted/test/repo_test':
        return MockResponse({'rate':'0.7'}, 200)
    elif args[0] == URL_PR + 'acceptance_quality/test/repo_test':
        return MockResponse({'metric':'0,6'}, 200)

    

    return MockResponse(None, 404)


class HubcareApiViewTest(TestCase):
    '''
    Test Hubcare API
    '''
    def setup(self):
        '''
        setup test configs
        '''
        pass

    