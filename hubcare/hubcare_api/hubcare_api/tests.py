from django.test import RequestFactory, TestCase
from hubcare_api.indicators import active_indicator
from hubcare_api.indicators import welcoming_indicator
from hubcare_api.indicators import support_indicator
from hubcare_api.views import HubcareApiView
from hubcare_api.constants import *
from unittest import mock


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

    cont_authors = 'contributors/test/repo_test'

    if args[0] == active_indicator.get_active_indicator('test', 'repo_test'):
        return MockResponse({
                'active_metric': 0.9287
                # 'welcoming_metric': 0.9287,
                # 'support_metric': 0.9287,
            },
            200
        )
    # elif args[0] == URL_COMMUNITY + 'code_of_conduct/test/repo_test':
    #     return MockResponse({'code_of_conduct': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'contribution_guide/test/repo_test':
    #     return MockResponse({'contribution_guide': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'description/test/repo_test':
    #     return MockResponse({'description': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'issue_template/test/repo_test':
    #     return MockResponse({'issue_templates': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'license/test/repo_test':
    #     return MockResponse({'have_license': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'pull_request_template/test/repo_test':
    #     return MockResponse({'pull_request_template': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'readme/test/repo_test':
    #     return MockResponse({'readme': 'True'}, 200)
    # elif args[0] == URL_COMMUNITY + 'release_note/test/repo_test':
    #     return MockResponse({'response': 'True'}, 200)
    # elif args[0] == URL_COMMIT + 'commit_week/test/repo_test':
    #     return MockResponse({'sum': '273'}, 200)
    # elif args[0] == URL_COMMIT + cont_authors:
    #     return MockResponse([
    #             {'author': 'CleberHiroshi23@gmail.com', 'numberCommits': 7},
    #             {'author': 'Toyoshima321@hotmail.com', 'numberCommits': 5},
    #             {'author': 'JacoVitor33@orkut.com', 'numberCommits': 2},
    #             {'author': 'RomulanoFranchesco@msn.com', 'numberCommits': 10},
    #         ],
    #         200
    #     )
    # elif args[0] == URL_ISSUE + 'activity_rate/test/repo_test':
    #     return MockResponse({'activity_rate_15_days': '1'}, 200)
    # elif args[0] == URL_ISSUE + 'good_first_issue/test/repo_test':
    #     return MockResponse({'rate': '0.8'}, 200)
    # elif args[0] == URL_ISSUE + 'help_wanted/test/repo_test':
    #     return MockResponse({'rate': '0.7'}, 200)
    # elif args[0] == URL_PR + 'acceptance_quality/test/repo_test':
    #     return MockResponse({'metric': '0.6'}, 200)

    return MockResponse(None, 404)


class HubcareApiTest(TestCase):
    '''
    test all methods to view class
    '''
    def setup(self):
        '''
        setup test configs
        '''
        self.factory = RequestFactory()

    @mock.patch(
        'hubcare_api.views.requests.get',
        side_effect=mocked_requests_get
    )
    def test_repository_not_existance(self, mock_get):
        '''
        test if a hubcare_api exists in github api
        '''
        response = HubcareApiView.as_view()(
            RequestFactory().get('hubcare_indicators/cleber/cremilda'),
            'cleber',
            'cremilda'
        )
        self.assertEqual(response.status_code, 404)
    
    @mock.patch(
        'hubcare_api.views.active_indicator.get_active_indicator',
        side_effect=mocked_requests_get
    )
    def test_hubcare_api(self, mock_get):
        '''
        test if hubcare API return: active indicator
        '''
        response = HubcareApiView.as_view()(
            RequestFactory().get('hubcare_indicators/test/repo_test'),
            'test',
            'repo_test'
        )
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(active_indicator.get_active_indicator(), 0.50097)
        #self.assertEqual(response.data['welcoming_indicator'], 0.60)
        #self.assertEqual(response.data['support_indicator'], 0.70)


