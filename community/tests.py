from django.test import RequestFactory, TestCase
from .models import License
from .views import LicenseView
from datetime import date

class LicenseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.license = License.objects.create(
            owner='cleber', repo='cremilda', have_license=True, date=date.today()
        )
    
    def test_details(self):
        request = self.factory.get('/community/license/cleber/cremilda')

        # request.license = self.license

        # response = LicenseView().get(request,owner='cleber',repo='cremilda')
        # response = LicenseView(request)
        response = LicenseView.as_view()(request, 'cleber', 'cremilda')
        self.assertEqual(response.status_code, 200)