from django.test import TestCase, RequestFactory
from contributors.models import DifferentsAuthors
from contributors.views import DifferentsAuthorsView
from datetime import datetime, timezone, date
from unittest import mock


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(None, 404)


class DifferentsAuthorsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.differentsauthors = DifferentsAuthors.objects.create(
            owner='cleber',
            repo='cremilda'
        )

    @mock.patch('differentauthors.views.requests_get',
                side_effect=mocked_requests_get)
    def test_repository_not_existence(self, mock_get):
        request = self.factory.get('different_authors/cleber/cremilda')
        response = DifferentsAuthorsView.as_view()(
            request,
            'cleber',
            'cremilda'
            )
        self.assertEqual(response.status_code, 404)

    def test_exists_in_db(self):
        request = self.factory.get('different_authors/cleber/cremilda')
        response = DifferentsAuthorsView.as_view()(
            request,
            'cleber',
            'cremilda'
            )
        self.assertEqual(response.status_code, 200)

    @mock.patch('differentauthors.views.requests.get',
                side_effect=mocked_requests_get)
