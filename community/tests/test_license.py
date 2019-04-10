from django.test import RequestFactory, TestCase
from community.models.license_model import License
from community.views.license_view import LicenseView
from datetime import date
from unittest import mock


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    # if args[0] == 'http://someurl.com/test.json':
    #     return MockResponse({"key1": "value1"}, 200)
    # elif args[0] == 'http://someotherurl.com/anothertest.json':
    #     return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)

class LicenseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.license = License.objects.create(
            owner='cleber',
            repo='cremilda',
            have_license=True,
            date=date.today(),
        )

    @mock.patch('community.views.license_view.requests.get', side_effect=mocked_requests_get)
    def test_RepositoryExistence(self, mock_get):
        request = self.factory.get('/community/license/cleber/desenho')
        response = LicenseView.as_view()(request, 'cleber', 'desenho')
        self.assertEqual(response.status_code, 404)

    def test_LicenseTrue(self):
        request = self.factory.get('/community/license/cleber/cremilda')
        response = LicenseView.as_view()(request, 'cleber', 'cremilda')
        self.assertEqual(response.status_code, 200)
