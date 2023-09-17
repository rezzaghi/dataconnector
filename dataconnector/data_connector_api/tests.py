import environ
from django.test import TestCase
from rest_framework.test import APIClient
from .models import *

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


class TransactionTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.transactions_data = [
            {
                'actions': '',
                'transaction_type': 'Market - Buy',
                'symbol': 'K',
                'quantity': 3,
                'type': 'Equities',
                'price_status': '60.0500',
                'fee': '1.00',
                'date_time': '09/15/2023 - 12:52',
            },
            {
                'actions': '',
                'transaction_type': 'Market - Buy',
                'symbol': 'AAPL',
                'quantity': 2,
                'type': 'Equities',
                'price_status': '174.9300',
                'fee': '1.00',
                'date_time': '09/15/2023 - 12:51',
            },
        ]
        Transaction.objects.record_data_collected(self.transactions_data, self.username)

    def test_record_data_collected(self):
        # Check if the transactions have been recorded correctly
        transaction1 = Transaction.objects.get(userName=self.username, symbol='K')
        self.assertEqual(transaction1.actions, '')
        self.assertEqual(transaction1.transaction_type, 'Market - Buy')
        self.assertEqual(transaction1.quantity, 3)
        self.assertEqual(transaction1.type, 'Equities')
        self.assertEqual(float(transaction1.price_status), 60.0500)
        self.assertEqual(float(transaction1.fee), 1.00)
        self.assertEqual(
            transaction1.date_time.strftime("%m/%d/%Y - %H:%M"),
            '09/15/2023 - 12:52'
        )

        transaction2 = Transaction.objects.get(userName=self.username, symbol='AAPL')
        self.assertEqual(transaction2.actions, '')
        self.assertEqual(transaction2.transaction_type, 'Market - Buy')
        self.assertEqual(transaction2.quantity, 2)
        self.assertEqual(transaction2.type, 'Equities')
        self.assertEqual(float(transaction2.price_status), 174.9300)
        self.assertEqual(float(transaction2.fee), 1.00)
        self.assertEqual(
            transaction2.date_time.strftime("%m/%d/%Y - %H:%M"),
            '09/15/2023 - 12:51'
        )

    def test_get_transactions_within_date_range(self):
        # Get transactions within a date range
        start_date = datetime.strptime("09/15/2023 - 12:51", "%m/%d/%Y - %H:%M") 
        end_date = datetime.strptime("09/16/2023 - 12:52", "%m/%d/%Y - %H:%M") 

        transactions_within_range = Transaction.objects.get_transactions_within_date_range(
            start_date, end_date, self.username
        )

        # Check if the transactions retrieved are within the specified date range
        self.assertEqual(len(transactions_within_range), 2)

        for transaction in transactions_within_range:
            date_time = datetime.strptime(transaction['date_time'], "%m/%d/%Y - %H:%M")
            self.assertTrue(start_date <= date_time <= end_date)

    def test_get_transactions_within_date_range_empty(self):
        # Get transactions within an empty date range
        start_date = datetime.strptime("01/01/3000 - 14:45", "%m/%d/%Y - %H:%M") 
        end_date = datetime.strptime("01/01/3000 - 14:45", "%m/%d/%Y - %H:%M") 

        transactions_within_range = Transaction.objects.get_transactions_within_date_range(
            start_date, end_date, self.username
        )

        self.assertEqual(len(transactions_within_range), 0)