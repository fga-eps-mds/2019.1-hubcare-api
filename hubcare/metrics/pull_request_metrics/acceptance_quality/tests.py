from django.test import TestCase, RequestFactory
from acceptance_quality.models import PullRequestQuality
from acceptance_quality.views import PullRequestQualityView
from datetime import datetime, timezone
from unittest import mock


def mocked_requests_get(*args, **kwargs):
    '''
        This method will be used by the mock to replace requests.get
    '''
    class MockResponse:
        '''
            Define response to mock request
        '''


class PullRequestQualityViewTest(TestCase):
    '''
        Test all methods to view class
    '''
    def setUp(self):
        '''
            Setup test configs
        '''
        self.factory = RequestFactory()
        self.pullrequestquality = PullRequestQuality.objects.create()

    @mock.patch('pullrequestquality.views.requests.get',
                side_effect=mocked_requests_get)
    def test_pull_request_quality_existence(self, mock_get):
        '''
            Test if the pull request quality already exists
        '''

    def test_pull_request_quality_existence_in_db(self):
        '''
            Test if there is pull request quality at db
        '''

    @mock.patch('license.views.request.get',
                side_effect=mocked_requests_get)
    def test_check_datetime_out(self, mock_get):
        '''
            Test if already has a score based on PRs
        '''
    @mock.patch('license.views.request.get',
                side_effect=mocked_requests_get)
    def test_check_datetime(self, mock_get):
        '''
            Test if the score it that old
        '''
