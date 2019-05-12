from django.test import RequestFactory, TestCase
from readme.models import Readme
from readme.views import ReadmeView
from datetime import datetime, timezone
from unittest import mock


def mocked_requests_get(*args, **kwargs):
    '''
    This method will be used by th mock to replace requests.get
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
            return all datas in objects
            '''
            return self.json_data

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api'
    url2 = 'https://api.github.com/repos/owner_date/repo_date'
    url_content = '/contents/README.md'
    if args[0] == url1 + url_content:
        return MockResponse({"README": "name"}, 200)
    elif args[0] == url2 + url_content:
        return MockResponse({"README": "name"}, 200)
    return MockResponse(None, 404)


class ReadmeViewTest(TestCase):
    def setUp(self):
        '''
        Define Readme objects to tests
        '''
        self.factory = RequestFactory()
        Readme.objects.create(
            owner='owner_test',
            repo='repo_test',
            readme=True,
            date_time=datetime.now(timezone.utc)
        )
        Readme.objects.create(
            owner='owner_date',
            repo='repo_date',
            readme=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )
        Readme.objects.create(
            owner='owner_date2',
            repo='repo_date2',
            readme=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )

    def test_readme_existence_in_db(self):
        '''
        test if there is readme in the local database
        '''
        url = 'readme/owner_test/repo_test'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(
            request,
            'owner_test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_readme_existence(self, mock_get):
        '''
        test if readme existence in github api
        '''
        url = 'readme/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(
            request,
            'fga-eps-mds',
            '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['readme'], True)

    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_readme_not_existence(self, mock_get):
        '''
        test if readme not existence in github api
        '''
        url = 'readme/not_exists/not_exists'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(
            request,
            'not_exists',
            'not_exists'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_exists')
        self.assertEqual(response.data['repo'], 'not_exists')
        self.assertEqual(response.data['readme'], False)

    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_date_readme_existence(self, mock_get):
        '''
        test old date of readme in database
        '''
        url = 'readme/owner_date/repo_date'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(
            request,
            'owner_date',
            'repo_date'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date')
        self.assertEqual(response.data['repo'], 'repo_date')
        self.assertEqual(response.data['readme'], True)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))

    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_date_readme_not_existence(self, mock_get):
        '''
        test old date of readme in database
        and the readme not exists
        '''
        url = 'readme/owner_date2/repo_date2'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(
            request,
            'owner_date2',
            'repo_date2'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date2')
        self.assertEqual(response.data['repo'], 'repo_date2')
        self.assertEqual(response.data['readme'], False)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
