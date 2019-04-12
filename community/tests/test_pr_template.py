from django.test import TestCase, RequestFactory
from community.models.pr_template_model import Community
from community.views.pr_template_view import PullRequestTemplateView
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
    url2 = 'contents/.github/PULL_REQUEST_TEMPLATE.md'
    if args[0] == url1 + url2:
        return MockResponse({'PULL_REQUEST_TEMPLATE': 'name'}, 200)

    return MockResponse(None, 404)


class TestCommunity(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pull_request_template = Community.objects.create(
            owner='ownertest',
            repo='repositest',
            has_pull_request_template=True,
            date_time='2018-05-04'
        )
    
    def test_exists_in_db(self):
        '''
        test if there is pull request template in the local database
        '''
        request = self.factory.get('/community/pull_request_template/owner_test/repo_test')
        response = PullRequestTemplateView.as_view()(request, 'owner_test', 'repo_test')
        self.assertEqual(response.status_code, 200)

    @mock.patch('community.views.pr_template_view.requests.get',
                side_effect=mocked_reques_get)
    
    def test_pull_request_template_exists(self, mock_get):
        url = '/pull_request_template/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)

        response = PullRequestTemplateView.as_view()(
                                                    request,
                                                    'fga-eps-mds',
                                                    '2019.1-hubcare-api')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['pull_request_template'], True)

    @mock.patch('community.views.pr_template_view.requests.get',
                side_effect=mocked_reques_get)
    
    def test_pull_request_template_not_exists(self, mock_get):
        request = self.factory.get('/pull_request_template/test/repo_test')

        response = PullRequestTemplateView.as_view()(
                                                    request,
                                                    'test',
                                                    'repo_test')                

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'test')
        self.assertEqual(response.data['repo'], 'repo_test')
        self.assertEqual(response.data['pull_request_template'], False)
    
    @mock.patch('community.views.pr_template_view.requests.get', side_effect=mock)

    def test_date_pull_request_template_exists(self, mock_get):
        resquest = self.factory.get('/pull_request_template/ownertest/repositest')

        response = PullRequestTemplateView.as_view()(request,  'ownertest', 'repositest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'ownertest')
        self.assertEqual(response.data['repo'], 'repositest')
        self.assertEqual(response.data['pull_request_template'], True)
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
    