from django.test import RequestFactory, TestCase
from community.models.license_model import License
from community.views.license_view import LicenseView
from datetime import date


class LicenseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.license = License.objects.create(
            owner='cleber',
            repo='cremilda',
            have_license=True,
            date=date.today(),
        )

    def test_RepositoryExistence(self):
        request = self.factory.get('/community/license/cleber/cremilda')
        response = LicenseView.as_view()(request, 'cleber', 'desenho')
        self.assertEqual(response.status_code, 404)

    def test_LicenseTrue(self):
        request = self.factory.get('/community/license/cleber/cremilda')
        response = LicenseView.as_view()(request, 'cleber', 'cremilda')
        self.assertEqual(response.status_code, 200)
