from django.test import RequestFactory, TestCase
from readme.models import Readme
from readme.views import ReadmeView
from unittest import mock
from datetime import date


def mocked_requests_get(*args, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):

            return self.json_data

    url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api'
    contents = '/contents/README.md'
    if args[0] == url1 + contents:
        return MockResponse({"readme": "name"}, 200)
    return MockResponse(None, 404)


class ReadmeViewTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.readme = Readme.objects.create(
            owner='owner_test',
            repo='repo_test',
            readme=True,
            date=date.today()
        )
    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_readme_existence(self, mock_get):

        url = 'readme/fga-eps-mds/2019.1-hubcare-api'
        fga_url = 'fga-eps-mds'
        hubcare_url = '2019.1-hubcare-api'
        request = self.factory.get(url)
        response = ReadmeView.as_view()(request, fga_url, hubcare_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 'fga-eps-mds')
        self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
        self.assertEqual(response.data['readme'], True)
