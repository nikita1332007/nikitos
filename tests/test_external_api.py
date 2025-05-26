import unittest
from unittest.mock import patch, Mock
import requests

from src.external_api import convert_to_rub


class TestConvertToRub(unittest.TestCase):

    @patch('requests.get')
    def test_convert_usd_to_rub(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'result': 75.0}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction = {'amount': 100, 'currency': 'USD'}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 75.0)

    @patch('requests.get')
    def test_convert_eur_to_rub(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'result': 85.0}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction = {'amount': 100, 'currency': 'EUR'}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 85.0)

    @patch('requests.get')
    def test_convert_rub(self, mock_get):
        transaction = {'amount': 100, 'currency': 'RUB'}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)

    @patch('requests.get')
    def test_convert_unknown_currency(self, mock_get):
        transaction = {'amount': 100, 'currency': 'JPY'}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)

    @patch('requests.get')
    def test_api_error(self, mock_get):
        # Имитация ошибки API
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        transaction = {'amount': 100, 'currency': 'USD'}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)


if __name__ == '__main__':
    unittest.main()
