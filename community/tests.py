from django.test import TestCase
from .models import License
from django.utils import unittest
from django.test.client import RequestFactory

# Create your tests here.

class TestLicense(TestCase):

    def setUp(self):
        self.key = "mit"
        self.name = "MIT License"
        self.spdx_id = "MIT"
        self.url = "https://api.github.com/licenses/mit"
        self.node_id = "MDc6TGljZW5zZTEz" 

    def test_license_valid(self):
        form_data = {
            'key' = self.key,
            'name' = self.name,
            'spdx_id' = self.spdx_id,
            'url' = self.url,
            'node_id' = self.node_id
        }

        form = CreateCustomLicense(data=form_data)

        self.assertTrue(form.is_valid())