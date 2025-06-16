import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, mock_open


def expenses_by_category(df, category):
    total = df[df['Категория'] == category]['Сумма'].sum()
    with open('report_output.json', 'w') as f:
        f.write(str(total))
    return total


def weekly_expenses(df):
    weekly_exp = {day: 0.0 for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}

    for _, row in df.iterrows():
        day_name = row['Дата'].strftime('%A')
        weekly_exp[day_name] += row['Сумма']

    return {day: float(amount) for day, amount in weekly_exp.items()}


class TestExpenseFunctions(unittest.TestCase):
    def setUp(self):
        data = {
            'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения', 'Транспорт'],
            'Дата': [
                datetime(2023, 1, 15),  # Sunday
                datetime(2023, 2, 10),  # Friday
                datetime(2023, 3, 5),   # Sunday
                datetime(2023, 3, 20),  # Monday
                datetime(2023, 4, 1)    # Saturday
            ],
            'Сумма': [100, 50, 200, 150, 80]
        }
        self.df = pd.DataFrame(data)

    @patch('builtins.open', new_callable=mock_open)
    def test_expenses_by_category(self, mock_file):
        result = expenses_by_category(self.df, 'Еда')
        self.assertEqual(result, 300)  # Ожидаемая сумма: 100 + 200

        mock_file.assert_called_once_with('report_output.json', 'w')
        handle = mock_file()
        handle.write.assert_called_once_with('300')

    def test_weekly_expenses(self):
        expected_result = {
            'Sunday': 300.0,   # 100 + 200 (15 Jan + 5 Mar)
            'Monday': 150.0,   # 150 (20 Mar)
            'Tuesday': 0.0,
            'Wednesday': 0.0,
            'Thursday': 0.0,
            'Friday': 50.0,    # 50 (10 Feb)
            'Saturday': 80.0    # 80 (1 Apr)
        }

        result = weekly_expenses(self.df)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
