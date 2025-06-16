import json
import unittest
from src.services import analyze_cashback, investment_bank, search_transactions


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        self.data = [
            {
                'Дата операции': '2024-04-15',
                'Категория': 'Продукты',
                'Сумма операции': 1000,
                'Кэшбэк': 5,
                'Описание': 'Покупка в магазине'
            },
            {
                'Дата операции': '2024-04-20',
                'Категория': 'Рестораны',
                'Сумма операции': 2000,
                'Кэшбэк': 10,
                'Описание': 'Ужин'
            },
            {
                'Дата операции': '2024-05-05',
                'Категория': 'Продукты',
                'Сумма операции': 500,
                'Кэшбэк': 5,
                'Описание': 'Покупка овощей'
            },
            {
                'Дата операции': '2024-04-25',
                'Категория': 'Транспорт',
                'Сумма операции': 300,
                'Кэшбэк': 2,
                'Описание': 'Бензин'
            },
            {
                'Дата операции': '2024-04-26',
                'Категория': 'Рестораны',
                'Сумма операции': 1500,
                'Кэшбэк': 10,
                'Описание': 'Кофе и десерт'
            }
        ]

    def test_analyze_cashback(self):
        result = analyze_cashback(self.data, 2024, 4)
        cashback = json.loads(result)
        self.assertAlmostEqual(cashback['Продукты'], 1000 * 0.05)
        self.assertAlmostEqual(cashback['Рестораны'], (2000 + 1500) * 0.10)
        self.assertAlmostEqual(cashback['Транспорт'], 300 * 0.02)

        cashback_may = json.loads(analyze_cashback(self.data, 2024, 5))
        self.assertAlmostEqual(cashback_may['Продукты'], 500 * 0.05)

    def test_investment_bank(self):
        saved = investment_bank('2024-04', self.data, 100)
        self.assertEqual(saved, 400)

        saved_may = investment_bank('2024-05', self.data, 100)
        self.assertEqual(saved_may, 100)

    def test_search_transactions(self):
        coffee_result = json.loads(search_transactions(self.data, 'кофе'))
        self.assertEqual(len(coffee_result), 1)
        self.assertEqual(coffee_result[0]['Описание'], 'Кофе и десерт')

        products_result = json.loads(search_transactions(self.data, 'Продукты'))
        self.assertEqual(len(products_result), 2)

        empty_result = json.loads(search_transactions(self.data, 'не существует'))
        self.assertEqual(len(empty_result), 0)


if __name__ == '__main__':
    unittest.main()
