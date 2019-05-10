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
    
    if args[0] == 'https://api.github.com/repos/test/repo_test/stats/participation':
        return MockResponse({"all":[
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                1,
                                18,
                                44,
                                70,
                                86,
                                73,
                                0]}, 
                            200)

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
            owner='cleber',
            repo='cremilda',
            date='2019-03-19'
        )

    @mock.patch('commit_week.views.requests.get',
                side_effect=mocked_requests_get)
    def test_repository_not_existence(self, mock_get):
        '''
        test if not exist repository in github api
        '''
        request = self.factory.get('commit_week/commit_week/cleber/desenho')
        response = CommitMonthView.as_view()(request, 'cleber', 'desenho')
        self.assertEqual(response.status_code, 404)

    def test_exists_in_db(self):
        '''
        test if a repository data exists in local db
        '''
        request = self.factory.get('commit_week/commit_week/cleber/cremilda')
        response = CommitMonthView.as_view()(request, 'cleber', 'cremilda')
        self.assertEqual(response.status_code, 200)

    @mock.patch('commit_week.views.requests.get',
                side_effect=mocked_requests_get)
    def test_sum(self, mock_get):
        '''
            test sum 
        '''
        request = self.factory.get('commit_week/commit_week/test/repo_test')
        response = CommitMonthView.as_view()(request, 'test', 'repo_test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'],'test')
        self.assertEqual(response.data['repo'],'repo_test')
        self.assertEqual(response.data['sum'],273)