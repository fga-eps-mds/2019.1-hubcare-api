import requests


class Request():
    def get(self, url):
        response = requests.get(url).json()
        return response

    def post(self, url):
        response = requests.post(url).json()
        return response

    def put(self, url):
        response = requests.put(url).json()
        return response
