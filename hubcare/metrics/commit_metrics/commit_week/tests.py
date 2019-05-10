from django.test import RequestFactory, TestCase
from unittest import mock
from datetime import datetime
from commit_metrics.models import Commit
from commit_week.models import CommitWeek
from commit_week.views import CommitMonthView
from commit_week.constants import *


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
    
    return MockResponse(None, 404)

class CommitMonthViewTest(TestCase):
    '''
    test all methods to view class
    '''

    @mock.patch('commit_week.views.requests.get',
                side_effect=mocked_requests_get)
    def test_repository_not_existence(self, mock_get):
        '''
        test if not exist repository in github api
        '''
        request = self.factory.get('commit_week/commit_week/cleber/desenho')
        response = CommitMonthView.as_view()(request, 'cleber', 'desenho')
        self.assertEqual(response.status_code, 404)