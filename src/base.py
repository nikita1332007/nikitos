import csv
import json
import re
from collections import Counter

import pandas as pd


def search_operations(transactions, search_str):
    '''Ищет транзакции по описанию.'''
    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    return [op for op in transactions if pattern.search(op.get('description', ''))]


def count_transaction_types(transactions):
    """

       Подсчитывает количество транзакций по категориям.
    """
    category_counter = Counter(op.get('category', 'Неизвестно') for op in transactions)
    return dict(category_counter)


def read_json_file(file_path):
    """
        Читает данные из JSON-файла.

    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        return []


def read_csv_file(file_path):
    """
        Читает данные из CSV-файла.

    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            return list(reader)
    except Exception as e:
        print(f"Ошибка чтения CSV: {e}")
        return []


def read_xlsx_file(file_path):
    """
        Читает данные из XLSX-файла.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Ошибка чтения XLSX: {e}")
        return []
