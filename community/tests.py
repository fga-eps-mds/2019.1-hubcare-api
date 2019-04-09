from django.test import TestCase, RequestFactory
from .models import Community
from .views import PullRequestTemplateView

class TestCommunity(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        
    def test_community(self):
        request = self.factory.get('/pull_request_template/fga-eps-mds/2019.1-hubcare-api')

        response = PullRequestTemplateView.as_view()(request, 'fga-eps-mds', '2019.1-hucare-api')

        self.assertEqual(response.status_code, 200)
        

