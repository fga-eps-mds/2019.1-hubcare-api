from django.test import TestCase, RequestFactory
from contributors.models import DifferentsAuthors
from contributors.views import DifferentsAuthorsView
from datetime import datetime, timezone, date
from unittest import mock


def mocked_requests_get(*args, **kwargs):
    pass

class DifferentsAuthorsViewTest(TestCase):
    pass