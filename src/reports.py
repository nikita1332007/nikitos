import pandas as pd
import json
import logging
from functools import wraps
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


def log_report(filename="report_output.json"):
    """
        Декоратор для ведения журнала результатов работы функции и сохранения их в JSON-файл.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (pd.Series, pd.DataFrame)):
                result = result.to_dict()
            with open(filename, 'w') as f:
                json.dump(result, f)
            return result
        return wrapper
    return decorator


@log_report()
def expenses_by_category(df: pd.DataFrame, category: str, date: datetime = None):
    """
        Вычисляет общую сумму расходов по указанной категории за последние три месяца.
    """
    if date is None:
        date = datetime.now()
    three_months_ago = date - timedelta(days=90)
    filtered = df[(df['Категория'] == category) & (df['Дата'] >= three_months_ago)]

    return filtered['Сумма'].sum()


@log_report("weekly_expenses.json")
def weekly_expenses(df: pd.DataFrame, date: datetime = None):
    """
        Вычисляет средние расходы по дням недели за последние три месяца.
    """
    if date is None:
      date = datetime.now()
    three_months_ago = date - timedelta(days=90)
    recent_data = df[df['Дата'] >= three_months_ago]
    recent_data['День'] = recent_data['Дата'].dt.day_name()
    return recent_data.groupby('День')['Сумма'].mean().to_dict()
