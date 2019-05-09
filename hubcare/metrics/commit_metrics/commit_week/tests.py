from django.test import RequestFactory, TestCase
from unittest import mock
from datetime import datetime
from commit_metrics.models import Commit
from commit_week.models import CommitWeek
from commit_week.views import CommitMonthView

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

    if args[0] == 'https://api.github.com/repos/test/repo_test':
        return MockResponse({"commit_week": "value1"}, 200)
    elif args[0] == 'https://api.github.com/repos/test/no_commit_week':
        return MockResponse({"commit_week": None}, 200)
    elif args[0] == 'https://api.github.com/repos/test/old_commit_week':
        return MockResponse({"commit_week": "value1"}, 200)
    elif args[0] == 'https://api.github.com/repos/test/old_commit_week':
        return MockResponse({"commit_week": None}, 200)

    return MockResponse(None, 404)




class CommitMonthViewTest(TestCase):
    '''
        test all methods to view class
    '''

    def setUp(self):
        '''
            setup test configs
        '''
        self.factory = RequestFactory()
        commit_metric = self.commit_metric = Commit.objects.create(
            owner='vitor',
            repo='pricom',
            date='2019-03-19'
       )
        self.commit_week = CommitWeek.objects.create(
            week=1,
            quantity=5,
            commit=commit_metric
       )

    @mock.patch('commit_week.views.requests.get',
                side_effect=mocked_requests_get)
    
    def test_repository_not_exist(self, mock_get):
        '''
            test if a repository exists
        '''
        request = self.factory.get('commit_week/cleber/desenho')
        response = CommitMonthView.as_view()(request, 'cleber', 'desenho')
        self.assertEqual(response.status_code, 404)
