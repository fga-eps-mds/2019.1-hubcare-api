from django.test import TestCase, RequestFactory
from description.models import Description
from description.views import DescriptionView
from datetime import datetime, timezone
from unittest import mock


def mocked_request_get(*args, **kwargs):
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
            return all datas in objetct
            '''
            return self.json_data

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api'
    url2 = 'https://api.github.com/repos/not_exists/not_exists'
    url3 = 'https://api.github.com/repos/owner_date/repo_date'
    url4 = 'https://api.github.com/repos/owner_date2/repo_date2'
    if args[0] == url1:
        return MockResponse({'description': 'value'}, 200)
    elif args[0] == url2:
        return MockResponse({'description': None}, 200)
    elif args[0] == url3:
        return MockResponse({'description': 'value'}, 200)
    elif args[0] == url4:
        return MockResponse({'description': None}, 200)
    return MockResponse(None, 404)


class DescriptionViewTest(TestCase):
    def setUp(self):
        '''
        Define Description objects to tests
        '''
        self.factory = RequestFactory()
        Description.objects.create(
            owner='owner_test',
            repo='repo_test',
            description=True,
            date_time=datetime.now(timezone.utc)
        )
        Description.objects.create(
            owner='owner_date',
            repo='repo_date',
            description=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )
        Description.objects.create(
            owner='owner_date2',
            repo='repo_date2',
            description=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )
        Description.objects.create(
            owner='owner_out',
            repo='repo_out',
            description=False,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 76910)
        )
    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_repository_not_existence(self, mock_get):
        '''
        test if not exist repository in github api
        '''
        request = self.factory.get('/description/owner/repo')
        response = DescriptionView.as_view()(request, 'owner', 'repo')
        self.assertEqual(response.status_code, 404)

    def test_exists_in_db(self):
        '''
        test if there is description in the local database
        '''
        url = '/description/owner_test/repo_test'
        request = self.factory.get(url)
        response = DescriptionView.as_view()(
            request,
            'owner_test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_description_exists(self, mock_get):
        '''
        test if description exists in github api
        '''
        url = '/description/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = DescriptionView.as_view()(
             request,
             'fga-eps-mds',
             '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['description'], True)

    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_description_not_exists(self, mock_get):
        '''
        test if description not exists in github api
        '''
        url = '/description/not_exists/not_exists'
        request = self.factory.get(url)
        response = DescriptionView.as_view()(
            request,
            'not_exists',
            'not_exists'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_exists')
        self.assertEqual(response.data['repo'], 'not_exists')
        self.assertEqual(response.data['description'], False)

    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_check_datetime_out(self, mock_get):
        '''
        test if not exist repository in github api yet
        '''
        request = self.factory.get('/description/owner_out/repo_out')
        response = DescriptionView.as_view()(request, 'owner_out', 'repo_out')
        self.assertEqual(response.status_code, 404)

    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_date_description_existence(self, mock_get):
        '''
        test old date of description in database
        '''
        url = '/description/owner_date/repo_date'
        request = self.factory.get(url)
        response = DescriptionView.as_view()(
            request,
            'owner_date',
            'repo_date'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date')
        self.assertEqual(response.data['repo'], 'repo_date')
        self.assertEqual(response.data['description'], True)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))

    @mock.patch('description.views.requests.get',
                side_effect=mocked_request_get)
    def test_date_description_not_exists(self, mock_get):
        '''
        test old date of description in database and
        the description not exists
        '''
        url = '/description/owner_date2/repo_date2'
        request = self.factory.get(url)

        response = DescriptionView.as_view()(
            request,
            'owner_date2',
            'repo_date2'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date2')
        self.assertEqual(response.data['repo'], 'repo_date2')
        self.assertEqual(response.data['description'], False)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
