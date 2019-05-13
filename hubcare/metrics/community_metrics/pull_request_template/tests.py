from django.test import TestCase, RequestFactory
from pull_request_template.models import PullRequestTemplate
from pull_request_template.views import PullRequestTemplateView
from datetime import datetime, timezone
from unittest import mock


def mocked_reques_get(*args, **kwargs):
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

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api/'
    url2 = 'https://api.github.com/repos/owner_date/repo_date/'
    url_content = 'contents/.github/PULL_REQUEST_TEMPLATE.md'
    if args[0] == url1 + url_content:
        return MockResponse({'PULL_REQUEST_TEMPLATE': 'name'}, 200)
    elif args[0] == url2 + url_content:
        return MockResponse({'PULL_REQUEST_TEMPLATE': 'name'}, 200)

    return MockResponse(None, 404)


class TestPullRequestTemplateView(TestCase):
    def setUp(self):
        '''
        Define PullRequesTemplate objects to tests
        '''
        self.factory = RequestFactory()
        PullRequestTemplate.objects.create(
            owner='owner_test',
            repo='repo_test',
            pull_request_template=True,
            date_time=datetime.now(timezone.utc)
        )
        PullRequestTemplate.objects.create(
            owner='owner_date',
            repo='repo_date',
            pull_request_template=True,
            date_time=datetime(2018, 4, 10, 16, 29, 43, 79043)
        )
        PullRequestTemplate.objects.create(
            owner='owner_date2',
            repo='repo_date2',
            pull_request_template=True,
            date_time=datetime(2018, 4, 10, 16, 29, 43, 79043)
        )

    def test_exists_in_db(self):
        '''
        test if there is pull request template in the local database
        '''
        url = '/pull_request_template/owner_test/repo_test'
        request = self.factory.get(url)
        response = PullRequestTemplateView.as_view()(
            request,
            'owner_test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('pull_request_template.views.requests.get',
                side_effect=mocked_reques_get)
    def test_pull_request_template_exists(self, mock_get):
        '''
        test if pull request template exists in github api
        '''
        url = '/pull_request_template/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = PullRequestTemplateView.as_view()(
            request,
            'fga-eps-mds',
            '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['pull_request_template'], True)

    @mock.patch('pull_request_template.views.requests.get',
                side_effect=mocked_reques_get)
    def test_pull_request_template_not_exists(self, mock_get):
        '''
        test if pull request template not exists in github api
        '''
        url = '/pull_request_template/not_exists/not_exists'
        request = self.factory.get(url)
        response = PullRequestTemplateView.as_view()(
            request,
            'not_exists',
            'not_exists'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_exists')
        self.assertEqual(response.data['repo'], 'not_exists')
        self.assertEqual(response.data['pull_request_template'], False)

    @mock.patch('pull_request_template.views.requests.get',
                side_effect=mocked_reques_get)
    def test_date_pull_request_template_exists(self, mock_get):
        '''
        test old date of pull request template in database
        '''
        url = '/pull_request_template/owner_date/repo_date'
        request = self.factory.get(url)

        response = PullRequestTemplateView.as_view()(
            request,
            'owner_date',
            'repo_date'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date')
        self.assertEqual(response.data['repo'], 'repo_date')
        self.assertEqual(response.data['pull_request_template'], True)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))

    @mock.patch('pull_request_template.views.requests.get',
                side_effect=mocked_reques_get)
    def test_date_pull_request_template_not_exists(self, mock_get):
        '''
        test old date of pull request template in database and
        the PR template not exists
        '''
        url = '/pull_request_template/owner_date2/repo_date2'
        request = self.factory.get(url)

        response = PullRequestTemplateView.as_view()(
            request,
            'owner_date2',
            'repo_date2'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date2')
        self.assertEqual(response.data['repo'], 'repo_date2')
        self.assertEqual(response.data['pull_request_template'], False)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
