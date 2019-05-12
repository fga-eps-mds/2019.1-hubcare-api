from django.test import TestCase, RequestFactory
from contributors.models import DifferentsAuthors
from contributors.views import DifferentsAuthorsView
from datetime import datetime, timezone, date
from unittest import mock


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__ (self, json_data, status_code):
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
        pass
    
    def test_exists_in_db(self):
        pass

    @mock.patch('differentauthors.views.requests.get',
                side_effect=mocked_requests_get)
    