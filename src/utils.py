import json
import os
from typing import List, Dict


def load_transactions(json_path: str) -> List[Dict]:
    """
    Читает JSON файл с транзакциями.
    Если файл пуст, не найден или данные не являются списком - возвращает пустой список.
    """
    if not os.path.exists(json_path):
        return []

    try:
        with open(json_path, encoding='utf-8') as file:
            data = json.load(file)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, IOError):
        return []
