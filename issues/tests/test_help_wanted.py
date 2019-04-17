from django.test import TestCase, RequestFactory
from issues.views.help_wanted_views import HelpWantedView
from issues.models.help_wanted_models import HelpWanted
from datetime import datetime, timezone
from unittest import mock
# Create your tests here.


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


class HelpWantedTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.help_wanted = HelpWanted.objects.create(
            owner='jaco',
            repo='desenho',
            total_issues='10',
            help_wanted_issues='1',
            date_time=datetime.now(timezone.utc)
        )

    @mock.patch('issues.views.help_wanted_views.requests.get',
                side_effect=mocked_requests_get)
    def test_repository_not_existence(self, mock_get):
        '''
        test if not exist repository in github api
        '''
        url = '/issues/help_wanted/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = HelpWantedView.as_view()(
            request,
            'fga-eps-mds',
            '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 404)

    def test_exists_in_db(self):
        '''
        test if a HelpWanted exists in local db
        '''
        request = self.factory.get('/issues/help_wanted/jaco/desenho')
        response = HelpWantedView.as_view()(request, 'jaco', 'desenho')
        self.assertEqual(response.status_code, 200)
