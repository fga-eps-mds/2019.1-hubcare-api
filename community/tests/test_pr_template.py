from django.test import TestCase, RequestFactory
from community.models.pr_template_model import Community
from community.views.pr_template_view import PullRequestTemplateView
from unittest import mock


def mocked_reques_get(*args, **kwargs):
    '''
    This method will be used by the mock to replace requests.get
    '''
    class MockReponse:
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
        return MockReponse({'PULL_REQUEST_TEMPLATE': 'name'}, 200)

    return MockReponse(None, 404)


class TestCommunity(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
