from django.test import RequestFactory, TestCase
from issue_template.models import IssueTemplate
from issue_template.views import IssueTemplateView
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
    url2 = 'https://api.github.com/repos/owner_date/repo_date/'
    url_content = 'contents/.github/ISSUE_TEMPLATE'
    if args[0] == url1 + url_content:
        return MockResponse({"ISSUE_TEMPLATE": "name"}, 200)
    elif args[0] == url2 + url_content:
        return MockResponse({"ISSUE_TEMPLATE": "name"}, 200)
    return MockResponse(None, 404)


class IssueTemplateViewTest(TestCase):
    def setUp(self):
        '''
        Define Readme objects to tests
        '''
        self.factory = RequestFactory()
        IssueTemplate.objects.create(
            owner='fga-eps-mds',
            repo='2019.1-hubcare-api',
            issue_templates=True,
            date_time=datetime.now(timezone.utc)
        )
        IssueTemplate.objects.create(
            owner='owner_test',
            repo='repo_test',
            issue_templates=True,
            date_time=datetime.now(timezone.utc)
        )
        IssueTemplate.objects.create(
            owner='owner_date',
            repo='repo_date',
            issue_templates=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )
        IssueTemplate.objects.create(
            owner='owner_date2',
            repo='repo_date2',
            issue_templates=True,
            date_time=datetime(2018, 5, 8, 15, 30, 45, 78910)
        )

    def test_issue_template_existence_in_db(self):
        '''
        test if there is issue template in the local database
        '''
        url = 'issue_template/owner_test/repo_test'
        request = self.factory.get(url)
        response = IssueTemplateView.as_view()(
            request,
            'owner_test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch('issue_template.views.requests.get',
                side_effect=mocked_requests_get)
    def test_issue_template_existence(self, mock_get):
        '''
        test if issue template existence in github api
        '''
        url = 'issue_template/fga-eps-mds/2019.1-hubcare-api'
        request = self.factory.get(url)
        response = IssueTemplateView.as_view()(
            request,
            'fga-eps-mds',
            '2019.1-hubcare-api'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['issue_templates'], True)

    @mock.patch('issue_template.views.requests.get',
                side_effect=mocked_requests_get)
    def test_issue_template_not_existence(self, mock_get):
        '''
        test if issue template not existence in github api
        '''
        url = 'issue_template/not_exists/not_exists'
        request = self.factory.get(url)
        response = IssueTemplateView.as_view()(
            request,
            'not_exists',
            'not_exists'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'not_exists')
        self.assertEqual(response.data['repo'], 'not_exists')
        self.assertEqual(response.data['issue_templates'], False)

    @mock.patch('issue_template.views.requests.get',
                side_effect=mocked_requests_get)
    def test_date_issue_template_existence(self, mock_get):
        '''
        test old date of issue_template in database
        '''
        url = 'issue_template/owner_date/repo_date'
        request = self.factory.get(url)
        response = IssueTemplateView.as_view()(
            request,
            'owner_date',
            'repo_date'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date')
        self.assertEqual(response.data['repo'], 'repo_date')
        self.assertEqual(response.data['issue_templates'], True)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))

    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_date_issue_template_not_existence(self, mock_get):
        '''
        test old date of issue template in database
        and the issue template not exists
        '''
        url = 'issue_template/owner_date2/repo_date2'
        request = self.factory.get(url)
        response = IssueTemplateView.as_view()(
            request,
            'owner_date2',
            'repo_date2'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'owner_date2')
        self.assertEqual(response.data['repo'], 'repo_date2')
        self.assertEqual(response.data['issue_templates'], False)
        response_date = response.data['date_time']
        date_strp = datetime.strptime(response_date[0:10], "%Y-%m-%d").date()
        self.assertEqual(str(date_strp),
                         str(datetime.now(timezone.utc).date()))
