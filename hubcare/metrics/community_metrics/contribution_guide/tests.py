from django.test import RequestFactory, TestCase
from contribution_guide.models import ContributionGuide
from contribution_guide.views import ContributionGuideView
from datetime import date, timezone
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
            return all datas in objects
            '''
            return self.json_data

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api'
    contents = '/contents/.github/CONTRIBUTING.md'
    if args[0] == url1 + contents:
        return MockResponse({"contribution_guide": "name"}, 200)
    return MockResponse(None, 404)


class ContributionGuideViewTest(TestCase):
    def setUp(self):
        '''
        Define Contribution Guide objects to tests
        '''
        self.factory = RequestFactory()
        ContributionGuide.objects.create(
            owner='owner_test',
            repo='repo_test',
            contribution_guide=True,
            date=date.today()
        )

    def test_exists_in_db(self):
        '''
        test if there is contribution guide in the local database
        '''
        url = 'contribution_guide/owner_test/repo_test'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'owner_test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('contribution_guide.views.requests.get',
                side_effect=mocked_request_get)
    def test_contribution_guide_existence(self, mock_get):
        '''
        test if contribution guide existence in github api
        '''
        url = 'contribution_guide/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'fga-eps-mds',
            '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['contribution_guide'], True)

    @mock.patch('contribution_guide.views.requests.get',
                side_effect=mocked_request_get)
    def test_contribution_guide_not_existence(self, mock_get):
        '''
        test if contribution guide not existence in github api
        '''
        url = 'contribution_guide/not_exists/not_exists'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'not_exists',
            'not_exists'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_exists')
        self.assertEqual(response.data['repo'], 'not_exists')
        self.assertEqual(response.data['contribution_guide'], False)
