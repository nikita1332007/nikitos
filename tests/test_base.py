import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from src.base import search_operations, count_transaction_types, read_json_file, read_csv_file, read_xlsx_file


class TestOperations(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            {'description': 'Оплата за интернет', 'category': 'Коммунальные услуги'},
            {'description': 'Перевод между счетами', 'category': 'Банковские услуги'},
            {'description': 'Купить продукты', 'category': 'Супермаркет'},
            {'description': 'Оплата за коммуналку', 'category': 'Коммунальные услуги'},
        ]

    def test_search_operations(self):
        result = search_operations(self.transactions, 'интернет')
        self.assertEqual(len(result), 1)
        self.assertIn('Оплата за интернет', [op['description'] for op in result])

        result = search_operations(self.transactions, 'покупка')
        self.assertEqual(len(result), 0)

    def test_count_transaction_types(self):
        result = count_transaction_types(self.transactions)
        expected = {'Коммунальные услуги': 2, 'Банковские услуги': 1, 'Супермаркет': 1}
        self.assertEqual(result, expected)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"description": "Оплата", "category": "Тест"}]')
    def test_read_json_file(self, mock_file):
        result = read_json_file('test.json')
        expected = [{'description': 'Оплата', 'category': 'Тест'}]
        self.assertEqual(result, expected)

        mock_file.side_effect = FileNotFoundError
        result = read_json_file('invalid.json')
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='description;category\nОплата;Тест')
    def test_read_csv_file(self, mock_file):
        result = read_csv_file('test.csv')
        expected = [{'description': 'Оплата', 'category': 'Тест'}]
        self.assertEqual(result, expected)

        mock_file.side_effect = Exception("Ошибка чтения")
        result = read_csv_file('invalid.csv')
        self.assertEqual(result, [])

    @patch('pandas.read_excel')
    def test_read_xlsx_file(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({'description': ['Оплата'], 'category': ['Тест']})
        result = read_xlsx_file('test.xlsx')
        expected = [{'description': 'Оплата', 'category': 'Тест'}]
        self.assertEqual(result, expected)

        mock_read_excel.side_effect = Exception("Ошибка чтения")
        result = read_xlsx_file('invalid.xlsx')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
