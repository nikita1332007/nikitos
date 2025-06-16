import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime

from src.views import get_date_range, get_greeting, filter_operations_by_date, aggregate_cards, top_transactions, get_currency_rates, get_stock_prices


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        # Подготовка DataFrame для тестов
        self.df = pd.DataFrame({
            'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-10', '2020-05-20']),
            'Дата платежа': pd.to_datetime(['2020-05-02', '2020-05-11', '2020-05-21']),
            'Статус': ['OK', 'FAILED', 'OK'],
            'Номер карты': ['1234', '1234', '5678'],
            'Сумма платежа': [150.5, 200, 50],
            'Валюта платежа': ['RUB', 'RUB', 'RUB'],
            'Описание': ['Покупка1', 'Покупка2', 'Покупка3']
        })

    def test_get_date_range(self):
        dt = datetime(2020, 5, 20, 14, 30)
        start, end = get_date_range(dt)
        self.assertEqual(start, datetime(2020, 5, 1).date())
        self.assertEqual(end, datetime(2020, 5, 20).date())

    def test_get_greeting(self):
        self.assertEqual(get_greeting(datetime(2020, 5, 20, 5, 0)), "Доброй ночи")
        self.assertEqual(get_greeting(datetime(2020, 5, 20, 6, 0)), "Доброе утро")
        self.assertEqual(get_greeting(datetime(2020, 5, 20, 12, 0)), "Добрый день")
        self.assertEqual(get_greeting(datetime(2020, 5, 20, 18, 0)), "Добрый вечер")

    def test_filter_operations_by_date(self):
        filtered = filter_operations_by_date(self.df, datetime(2020, 5, 1).date(), datetime(2020, 5, 10).date())
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(filtered['Дата операции'].dt.date <= datetime(2020, 5, 10).date()))

    def test_aggregate_cards(self):
        cards = aggregate_cards(self.df)
        expected = [
            {'card_number': '1234', 'total_expenses': 150.5, 'cashback': 1},
            {'card_number': '5678', 'total_expenses': 50.0, 'cashback': 0}
        ]
        self.assertEqual(cards, expected)

    def test_top_transactions(self):
        top = top_transactions(self.df, top_n=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]['payment_amount'], 150.5)
        self.assertEqual(top[1]['payment_amount'], 50.0)

    @patch('requests.get')
    def test_get_currency_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {'USD': 0.013, 'EUR': 0.011}
        }
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        rates = get_currency_rates(symbols=['USD', 'EUR'])
        self.assertEqual(rates, {'USD': 0.013, 'EUR': 0.011})

    @patch('requests.get')
    def test_get_stock_prices(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'quoteResponse': {
                'result': [
                    {'symbol': 'AAPL', 'regularMarketPrice': 300.5},
                    {'symbol': 'GOOG', 'regularMarketPrice': 1400.7}
                ]
            }
        }
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        prices = get_stock_prices(['AAPL', 'GOOG'])
        self.assertEqual(prices, {'AAPL': 300.5, 'GOOG': 1400.7})


if __name__ == '__main__':
    unittest.main()
