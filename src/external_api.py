import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('EXCHANGE_API_KEY')
API_URL = 'https://api.apilayer.com/exchangerates_data/convert'


def convert_to_rub(transaction: dict) -> float:
    """
    Принимает транзакцию, возвращает сумму в рублях.
    Если валюта USD или EUR, конвертирует через API.
    При ошибках возвращает сумму без конвертации.
    """
    amount = transaction.get('amount', 0)
    currency = transaction.get('currency', 'RUB').upper()

    if currency == 'RUB':
        return float(amount)

    if currency not in ['USD', 'EUR']:

        return float(amount)

    if not API_KEY:
        raise ValueError("API key is not set in environment variables")

    headers = {
        'apikey': API_KEY
    }
    params = {
        'from': currency,
        'to': 'RUB',
        'amount': amount,
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        return float(result['result'])
    except (requests.RequestException, KeyError, ValueError):

        return float(amount)
