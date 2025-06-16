import json
from datetime import datetime
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)


def analyze_cashback(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
       Анализирует суммы кэшбэка по категориям за указанный месяц и год.
    """
    cashback_dict = {}
    for transaction in data:
        date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
        if date.year == year and date.month == month:
            category = transaction['Категория']
            cashback = transaction['Сумма операции'] * transaction['Кэшбэк'] / 100
            cashback_dict[category] = cashback_dict.get(category, 0) + cashback
    return json.dumps(cashback_dict)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
        Вычисляет общую сумму сэкономленных средств, округляя суммы транзакций до ближайшего лимита.
    """
    total_saved = 0
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
        if transaction_date.strftime('%Y-%m') == month:
            rounded_amount = (transaction['Сумма операции'] // limit + 1) * limit
            total_saved += rounded_amount - transaction['Сумма операции']
    return total_saved


def search_transactions(data: List[Dict[str, Any]], search_string: str) -> str:
    """
        Ищет транзакции по строке поиска, совпадающей с описанием или категорией.
    """
    results = [
        transaction for transaction in data
        if search_string.lower() in transaction['Описание'].lower() or
        search_string.lower() in transaction['Категория'].lower()
    ]
    return json.dumps(results)
