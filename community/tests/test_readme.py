from community.views import ReadmeView
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from community.models.readme_model import Readme

class ReadmeTest(APITestCase):
    def readme_exists(self):
        factory = APIRequestFactory()
        request = factory.get('/community/readme/vitormeirelesoliveira/scan_tcc/', {
  "name": "README.md",
  "path": "README.md",
  "sha": "7df641301667a5828dd26759fefb8761768561c8",
  "size": 266,
  "url": "https://api.github.com/repos/VitorMeirelesOliveira/scan_tcc/contents/README.md?ref=master",
  "html_url": "https://github.com/VitorMeirelesOliveira/scan_tcc/blob/master/README.md",
  "git_url": "https://api.github.com/repos/VitorMeirelesOliveira/scan_tcc/git/blobs/7df641301667a5828dd26759fefb8761768561c8",
  "download_url": "https://raw.githubusercontent.com/VitorMeirelesOliveira/scan_tcc/master/README.md",
  "type": "file",
  "content": "IyBTY2FuX3RjYwpTY2FuX3RjYyBpcyBhbiBvcGVuIHNvdXJjZSBwcm9qZWN0\nLCB3aGljaCBtYWtlcyB1c28gb2YgYW4gb3BlbiBoYXJkd2FyZSwgUmFzcGJl\ncnJ5IFBpIDMgYW5kIGFuIGludGVyZmFjZSBidWlsZCB1c2luZyBRdDUgYW5k\nIGNvZGVkIHdpdGggUHl0aG9uLgoKIyMjIFJlcXVpcmVtZW50cwoKIyMjIyBT\nb2Z0d2FyZQoKKiBweXRob24gPj0gMy42CiogcHlxdDUKKiBRdDUKCiMjIyMg\nSGFyZHdhcmUKCiogUmFzcGJlcnJ5UGkgMwoqIFBpQ2FtZXJhIFYyCgo=\n",
  "encoding": "base64",
  "_links": {
    "self": "https://api.github.com/repos/VitorMeirelesOliveira/scan_tcc/contents/README.md?ref=master",
    "git": "https://api.github.com/repos/VitorMeirelesOliveira/scan_tcc/git/blobs/7df641301667a5828dd26759fefb8761768561c8",
    "html": "https://github.com/VitorMeirelesOliveira/scan_tcc/blob/master/README.md"
  }
        }, format='json')

    self.assertEqual(Readme.objects.count(), 1)

    def readme_not_exists(self):
        pass