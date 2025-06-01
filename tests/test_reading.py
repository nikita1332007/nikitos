import unittest
from unittest.mock import patch
import pandas as pd
from src.reading import read_csv, read_excel


class TestFileReadFunctions(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_read_csv(self, mock_read_csv):

        mock_read_csv.return_value = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})

        expected_output = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        result = read_csv('fake_path.csv')
        self.assertEqual(result, expected_output)

    @patch('pandas.read_excel')
    def test_read_excel(self, mock_read_excel):

        mock_read_excel.return_value = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})

        expected_output = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        result = read_excel('fake_path.xlsx')
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
