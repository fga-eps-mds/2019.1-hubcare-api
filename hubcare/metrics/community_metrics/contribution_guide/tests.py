from django.test import TestCase, RequestFactory
from contribution_guide.models import ContributionGuide
from contribution_guide.views import ContributionGuideView
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

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api/'
    url2 = 'https://api.github.com/repos/owner_date/repo_date/'
    url_content = 'contents/.github/CONTRIBUTING.md'
    if args[0] == url1 + url_content:
        return MockResponse({'CONTRIBUTING': 'name'}, 200)
    elif args[0] == url2 + url_content:
        return MockResponse({'CONTRIBUTING': 'name'}, 200)
    return MockResponse(None, 404)


class ContributionGuideViewTest(TestCase):
    def setUp(self):
        '''
        define contribution guide object to tests
        '''
        self.factory = RequestFactory()
        ContributionGuide.objects.create(
            owner='owner_test',
            repo='repo_test',
            contribution_guide=True,
            date_time=datetime.now(timezone.utc)
        )
        ContributionGuide.objects.create(
            owner='fga-eps-mds',
            repo='2019.1-hubcare-api',
            contribution_guide=True,
            date_time=datetime.now(timezone.utc)
        )
        ContributionGuide.objects.create(
            owner='owner_date',
            repo='repo_date',
            contribution_guide=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )
        ContributionGuide.objects.create(
            owner='owner_date2',
            repo='repo_date2',
            contribution_guide=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )

    def test_existence_in_db(self):
        '''
        test if there is contribution guide in local database
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
        test if contribution guide exists in github api
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
        test if contribution guide not exists in github api
        '''
        url = 'contribution_guide/not_owner/not_repo'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'not_owner',
            'not_repo'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_owner')
        self.assertEqual(response.data['repo'], 'not_repo')
        self.assertEqual(response.data['contribution_guide'], False)

    @mock.patch('contribution_guide.views.requests.get',
                side_effect=mocked_request_get)
    def test_date_contribution_guide_existence(self, mock_get):
        '''
        test old date of contribution guide in database
        '''
        url = 'contribution_guide/owner_date/repo_date'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'owner_date',
            'repo_date'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date')
        self.assertEqual(response.data['repo'], 'repo_date')
        self.assertEqual(response.data['contribution_guide'], True)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))

    @mock.patch('contribution_guide.views.requests.get',
                side_effect=mocked_request_get)
    def test_date_contribution_guide_not_existence(self, mock_get):
        '''
        test old date of contribution guide in database
        and the contribution guide not exists
        '''
        url = 'contribution_guide/owner_date2/repo_date2'
        request = self.factory.get(url)
        response = ContributionGuideView.as_view()(
            request,
            'owner_date2',
            'repo_date2'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date2')
        self.assertEqual(response.data['repo'], 'repo_date2')
        self.assertEqual(response.data['contribution_guide'], False)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
