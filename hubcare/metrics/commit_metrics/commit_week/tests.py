from django.test import RequestFactory, TestCase
from unittest import mock
from datetime import datetime
from commit_week.models import CommitWeek
from commit_week.views import CommitMonthView

def mocked_requests_get(*args, **kwargs):



class CommitMonthViewTest(TestCase):
    '''
        test all methods to view class
    '''

    def setUp(self):
        '''
            setup test configs
        '''
        self.factory = RequestFactory()
        self.commit_week = CommitWeek.objects.create(
            owner='brian',
            repo='eda2',
            date=datetime.now()
        )
        self.commit_week2 = CommitWeek.objects.create(
            owner='brian',
            repo='eda2',
            date=datetime.now()
        )
        self.commit_week3 = CommitWeek.objects.create(
            owner='brian',
            repo='eda2',
            date=datetime.now()
        )
        self.commit_week4 = CommitWeek.objects.create(
            owner='brian',
            repo='eda2',
            date=datetime.now()
        )

    @mock.patch('commit_week.views.requests.get',
                side_effect=mocked_requests_get)
    
    def test_repository_not_exist(self, mock_get):
        '''
            test if a repository exists
        '''
        request = self.factory.get('')