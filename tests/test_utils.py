import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("os.path.exists", return_value=True)
    def test_empty_transaction_list(self, mock_exists, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='{"not": "a list"}')
    @patch("os.path.exists", return_value=True)
    def test_non_list_data(self, mock_exists, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    @patch("os.path.exists", return_value=True)
    def test_valid_transactions(self, mock_exists, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [{"id": 1, "amount": 100}])

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
