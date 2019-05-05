from django.test import RequestFactory, TestCase
from readme.models import Readme
from readme.views import ReadmeView
from unittest import mock
from datetime import date

def mocked_requests_get(*args, **kwargs):

    class MockResponse:
        def __init__(self,json_data,status_code):
            self.json_data =  json_data
            self.status_code = status_code

        def json(self):

            return self.json_data
        
    if args[0] == 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api/contents/README.md':
        return MockResponse({"readme":"value1"}, 200)
    
class ReadmeViewTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.readme = Readme.objects.create(
            owner='vitor',
            repo ='treinamento_git',
            readme= True,
            date= date.today()
        )
    @mock.patch('readme.views.requests.get',
                side_effect=mocked_requests_get)
    def test_readme_existence(self,mock_get):

        request = self.factory.get('readme/vitor/treinamento_git')
        response = ReadmeView.as_view()(request,'vitor','treinamento_git')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['owner'],slice('vitor'))
        self.assertEqual(response.data['repo'],'treinamento_git')
        self.assertEqual(response.data['readme'],True)


