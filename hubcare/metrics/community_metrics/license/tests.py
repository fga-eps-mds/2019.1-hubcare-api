# from django.test import RequestFactory, TestCase
# from license.models import License
# from license.views import LicenseView
# from datetime import datetime, timezone
# from unittest import mock


# def mocked_requests_get(*args, **kwargs):
#     '''
#     This method will be used by the mock to replace requests.get
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
#             return all datas in object
#             '''
#             return self.json_data

#     if args[0] == 'https://api.github.com/repos/test/repo_test':
#         return MockResponse({"license": "value1"}, 200)
#     elif args[0] == 'https://api.github.com/repos/test/no_license':
#         return MockResponse({"license": None}, 200)
#     elif args[0] == 'https://api.github.com/repos/test/old_license':
#         return MockResponse({"license": "value1"}, 200)
#     elif args[0] == 'https://api.github.com/repos/test/old_license_false':
#         return MockResponse({"license": None}, 200)

#     return MockResponse(None, 404)


# class LicenseViewTest(TestCase):
#     '''
#     test all methods to view class
#     '''
#     def setUp(self):
#         '''
#         setup test configs
#         '''
#         self.factory = RequestFactory()
#         self.license = License.objects.create(
#             owner='cleber',
#             repo='cremilda',
#             have_license=True,
#             date_time=datetime.now(timezone.utc),
#         )
#         self.license2 = License.objects.create(
#             owner='test',
#             repo='old_license',
#             have_license=True,
#             date_time=datetime(2018, 4, 10, 16, 29, 43, 79043)
#         )
#         self.license3 = License.objects.create(
#             owner='test',
#             repo='old_license_false',
#             have_license=False,
#             date_time=datetime(2018, 4, 10, 16, 29, 43, 79043)
#         )
#         self.license4 = License.objects.create(
#             owner='brian',
#             repo='mds',
#             have_license=False,
#             date_time=datetime(2018, 4, 10, 16, 29, 43, 79043)
#         )

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_repository_not_existence(self, mock_get):
#         '''
#         test if not exist repository in github api
#         '''
#         request = self.factory.get('license/cleber/desenho')
#         response = LicenseView.as_view()(request, 'cleber', 'desenho')
#         self.assertEqual(response.status_code, 404)

#     def test_exists_in_db(self):
#         '''
#         test if a license exists in local db
#         '''
#         request = self.factory.get('license/cleber/cremilda')
#         response = LicenseView.as_view()(request, 'cleber', 'cremilda')
#         self.assertEqual(response.status_code, 200)

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_license_exists(self, mock_get):
#         '''
#         test if a license exists in github api
#         '''
#         request = self.factory.get('license/test/repo_test')
#         response = LicenseView.as_view()(request, 'test', 'repo_test')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'test')
#         self.assertEqual(response.data['repo'], 'repo_test')
#         self.assertEqual(response.data['have_license'], True)

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_license_not_exists(self, mock_get):
#         '''
#         test if a license not exists in github api
#         '''
#         request = self.factory.get('license/test/no_license')
#         response = LicenseView.as_view()(request, 'test', 'no_license')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'test')
#         self.assertEqual(response.data['repo'], 'no_license')
#         self.assertEqual(response.data['have_license'], False)

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_check_datetime_out(self, mock_get):
#         '''
#         test if not exist repository in github api yet
#         '''
#         request = self.factory.get('license/brian/mds')
#         response = LicenseView.as_view()(request, 'brian', 'mds')
#         self.assertEqual(response.status_code, 404)

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_check_datetime(self, mock_get):
#         '''
#         test the license old datetime with license
#         '''
#         request = self.factory.get('license/test/old_license')
#         response = LicenseView.as_view()(request, 'test', 'old_license')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'test')
#         self.assertEqual(response.data['repo'], 'old_license')
#         self.assertEqual(response.data['have_license'], True)
#         response_data = response.data['date_time']
#         date_strp = datetime.strptime(response_data[0:10], "%Y-%m-%d").date()
#         self.assertEqual(str(date_strp),
#                          str(datetime.now(timezone.utc).date()))

#     @mock.patch('license.views.requests.get',
#                 side_effect=mocked_requests_get)
#     def test_check_datetime_false(self, mock_get):
#         '''
#         test the license old datetime without license
#         '''
#         request = self.factory.get('license/test/old_license_false')
#         response = LicenseView.as_view()(request, 'test',
#                                          'old_license_false')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['owner'], 'test')
#         self.assertEqual(response.data['repo'], 'old_license_false')
#         self.assertEqual(response.data['have_license'], False)
#         response_data = response.data['date_time']
#         date_strp = datetime.strptime(response_data[0:10], "%Y-%m-%d").date()
#         self.assertEqual(str(date_strp),
#                          str(datetime.now(timezone.utc).date()))
