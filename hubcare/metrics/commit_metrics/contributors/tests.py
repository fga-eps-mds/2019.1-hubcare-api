from django.test import RequestFactory, TestCase
from unittest import mock
from datetime import datetime, timezone, date
from contributors.models import DifferentsAuthors
from contributors.views import DifferentsAuthorsView


def mocked_requests_get(*args, **kwargs):
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
            return all datas in object
            '''
            return self.json_data

    return MockResponse(None, 404)


class DifferentsAuthorsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('contributors.views.requests_get',
                side_effect=mocked_requests_get)
    def test_repository_not_existence(self, mock_get):
        request = self.factory.get('contributors/test/repo_test')
        response = DifferentsAuthorsView.as_view()(
            request,
            'test',
            'repo_test'
        )
        self.assertEqual(response.status_code, 404)

    # def test_exists_in_db(self):
    #     request = self.factory.get('different_authors/cleber/cremilda')
    #     response = DifferentsAuthorsView.as_view()(
    #         request,
    #         'cleber',
    #         'cremilda'
    #         )
    #     self.assertEqual(response.status_code, 200)

    # @mock.patch('differentauthors.views.requests.get',
    #             side_effect=mocked_requests_get)
