# from django.test import RequestFactory, TestCase
# from release_note.models import ReleaseNoteCheck
# from release_note.views import ReleaseNoteCheckView
# from datetime import datetime, timezone
# from unittest import mock


# def mocked_requests_get(*args, **kwargs):
#     '''
#     This method will be used by th mock to replace requests.get
#     '''
#     class MockResponse:
#         '''
#         define response to mock request
#         '''
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code

#         def json(self):
#             '''
#             return all datas in objects
#             '''
#             return self.json_data

#     url1 = 'https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api'
#     url2 = 'https://api.github.com/repos/owner_test/repo_test'
#     url3 = 'https://api.github.com/repos/not_exists/not_exists'
#     url_release = '/releases'
#     if args[0] == url1 + url_release:
#         return MockResponse({"release": "value"}, 200)
#     elif args[0] == url2 + url_release:
#         return MockResponse({"release": "value"}, 200)
#     elif args[0] == url3 + url_release:
#         return MockResponse({"release": None}, 200)
#     return MockResponse(None, 404)


# class ReleaseNoteCheckViewTest(TestCase):
#     def setUp(self):
#         '''
#         define release note objects to tests
#         '''
#         self.factory = RequestFactory()
#         ReleaseNoteCheck.objects.create(
#             owner='fga-eps-mds',
#             repo='2019.1-hubcare-api',
#             have_realease_note=True,
#             date=datetime.now(timezone.utc)
#         )
#         ReleaseNoteCheck.objects.create(
#             owner='owner_test',
#             repo='repo_test',
#             have_realease_note=True,
#             date=datetime.now(timezone.utc)
#         )
#         ReleaseNoteCheck.objects.create(
#             owner='not_exists',
#             repo='not_exists',
#             have_realease_note=True,
#             date=datetime.now(timezone.utc)
#         )

#     def test_release_note_existence_in_db(self):
#         '''
#         test if there is release note in the local database
#         '''
#         url = 'release_note/owner_test/repo_test'
#         request = self.factory.get(url)
#         response = ReleaseNoteCheckView.as_view()(
#             request,
#             'owner_test',
#             'repo_test'
#         )
#         self.assertEqual(response.status_code, 200)

#     @mock.patch('release_note.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_release_note_existence(self, mock_get):
#         '''
#         test if release note existence in github api
#         '''
#         url = 'release_note/fga-eps-mds/2019.1-hubcare-api'
#         request = self.factory.get(url)
#         response = ReleaseNoteCheckView.as_view()(
#             request,
#             'fga-eps-mds',
#             '2019.1-hubcare-api'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'fga-eps-mds')
#         self.assertEqual(response.data['repo'], '2019.1-hubcare-api')
#         self.assertEqual(response.data['have_realease_note'], True)

#     @mock.patch('release_note.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_release_note_not_existence(self, mock_get):
#         '''
#         test if release note not existence in github api
#         '''
#         url = 'release_note/not_exists/not_exists/'
#         request = self.factory.get(url)
#         response = ReleaseNoteCheckView.as_view()(
#             request,
#             'not_exists',
#             'not_exists'
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'not_exists')
#         self.assertEqual(response.data['repo'], 'not_exists')
#         self.assertEqual(response.data['have_realease_note'], False)
