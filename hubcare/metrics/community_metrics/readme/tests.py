from django.test import RequestFactory, TestCase
from readme.models import Readme
from readme.views import ReadmeView
from unittest import mock
from datetime import date


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
    contents = '/contents/README.md'
    if args[0] == url1 + contents:
        return MockResponse({"README": "name"}, 200)
    return MockResponse(None, 404)


class ReadmeViewTest(TestCase):
    def setUp(self):
        '''
        Define Readme objects to tests
        '''
        self.factory = RequestFactory()
        self.readme = Readme.objects.create(
            owner='owner_test',
            repo='repo_test',
            readme=True,
            date=date.today()
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
