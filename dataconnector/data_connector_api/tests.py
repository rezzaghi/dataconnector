import environ
from django.test import TestCase
from rest_framework.test import APIClient
env = environ.Env()

class WallStreetSurvivorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_wallstreetsurvivor_request_OK(self):
        url = '/wallstreetsurvivor/'
        data = {
            "username": env('USERNAME'),
            "password": env('PASSWORD'),
            "start_date": "2023-03-16",
            "end_date": "2023-09-16"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_wallstreetsurvivor_request_login_error(self):
        url = '/wallstreetsurvivor/'
        data = {
            "username": env('USERNAME'),
            "password": "WRONG",
            "start_date": "2023-03-16",
            "end_date": "2023-09-16"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.content, b'{"message": "Wrong credentials"}')

    def test_wallstreetsurvivor_request_missing_body_fields(self):
        url = '/wallstreetsurvivor/'
        data = {
            "username": env('USERNAME'),
            "start_date": "2023-03-16",
            "end_date": "2023-09-16"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.content, b'{"error": "Missing one or more required fields."}')