from django.test import TestCase, RequestFactory
from contributors.models import DifferentsAuthors
from contributors.views import DifferentsAuthorsView
from contributors.apps import ContributorsConfig
from django.apps import apps
from datetime import datetime, timezone
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

    if args[0] == 'https://api.github.com/repos/owner_test/repo_test/commits':
        # return MockResponse({"license": "value1"}, 200)
        return MockResponse(
            [
                {
                    "commit": {
                        "author": {
                            "name": "test",
                            "email": "test@test.com",
                            "date": "2019-05-15T16:27:43Z"
                        },
                        "committer": {
                            "name": "GitHub",
                            "email": "noreply@github.com",
                            "date": "2019-05-15T16:27:43Z"
                        }
                    }
                }
            ], 200)


    return MockResponse(None, 404)


class ContributorsViewTest(TestCase):
    '''
    test all methods to view class
    '''
    def setUp(self):
        '''
        setup test configs
        '''
        self.factory = RequestFactory()
    
    @mock.patch('contributors.views.requests.get',
                side_effect=mocked_requests_get)
    def test_license_exists(self, mock_get):
        '''
        test request to github api
        '''
        request = self.factory.get('contributors/owner_test/repo_test')
        response = DifferentsAuthorsView.as_view()(request, 'owner_test', 'repo_test')
        self.assertEqual(response.status_code, 200)


class ContributorsConfigTest(TestCase):
    '''
    test all methods to commit week configs class
    '''
    def test_config(self):
        self.assertEqual(ContributorsConfig.name, 'contributors')
        self.assertEqual(
            apps.get_app_config('contributors').name,
            'contributors'
        )