import json
import pandas as pd
import requests
from datetime import datetime, time
import logging


def load_operations(filename: str) -> pd.DataFrame:
    """
        Загружает операции из Excel файла.
    """
    df = pd.read_excel(filename)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True)
    return df


def get_date_range(input_datetime: datetime):
    """
        Получает диапазон дат на основе входной даты.
    """
    start_date = input_datetime.replace(day=1).date()
    end_date = input_datetime.date()
    return start_date, end_date


def load_user_settings(path='user_settings.json'):
    """
        Загружает настройки пользователя из JSON файла.
    """
    with open(path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    return settings


def get_greeting(input_datetime: datetime) -> str:
    """
        Генерирует приветствие в зависимости от времени суток.
    """
    current_time = input_datetime.time()
    if time(0, 0) <= current_time < time(6, 0):
        return "Доброй ночи"
    elif time(6, 0) <= current_time < time(12, 0):
        return "Доброе утро"
    elif time(12, 0) <= current_time < time(18, 0):
        return "Добрый день"
    else:
        return "Добрый вечер"


def filter_operations_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """
        Фильтрует операции по диапазону дат.
    """
    mask = (df['Дата операции'].dt.date >= start_date) & (df['Дата операции'].dt.date <= end_date)
    return df.loc[mask]


def aggregate_cards(df: pd.DataFrame):
    """
      Аггрегирует расходы по картам и вычисляет кэшбэк.
    """
    df_ok = df[df['Статус'] == 'OK']
    grouped = df_ok.groupby('Номер карты')['Сумма платежа'].sum()

    cards = []
    for card, total_sum in grouped.items():
        cashback = int(total_sum // 100)
        cards.append({
            'card_number': str(card),
            'total_expenses': round(float(total_sum), 2),
            'cashback': cashback
        })
    return cards


def top_transactions(df: pd.DataFrame, top_n=5):
    """
       Получает топ-N транзакций по сумме платежа.
    """
    df_ok = df[df['Статус'] == 'OK']
    df_sorted = df_ok.sort_values(by='Сумма платежа', ascending=False).head(top_n)

    transactions = []
    for _, row in df_sorted.iterrows():
        transactions.append({
            'date': row['Дата операции'].strftime('%Y-%m-%d'),
            'card_number': str(row['Номер карты']),
            'payment_amount': round(float(row['Сумма платежа']), 2),
            'payment_currency': row['Валюта платежа'],
            'description': row['Описание']
        })
    return transactions


def get_currency_rates(base='RUB', symbols=None):
    """
    Возвращает курсы валют к base.
    symbols - список валют для получения, например ['USD', 'EUR']
    """
    if symbols is None or len(symbols) == 0:
        return {}
    symbols_str = ','.join(symbols)
    url = f'https://api.exchangerate.host/latest?base={base}&symbols={symbols_str}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data.get('rates', {})
        return rates
    except Exception as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        return {}


def get_stock_prices(symbols):
    """
    Получает текущие цены акций по указанным символам.
    """
    if len(symbols) == 0:

        return {}
        symbols_str = ','.join(symbols)
        url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols_str}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            prices = {}
            for quote in data.get('quoteResponse', {}).get('result', []):
                symbol = quote.get('symbol')
                price = quote.get('regularMarketPrice')
                if symbol and price is not None:
                    prices[symbol] = float(price)
            return prices
        except Exception as e:
            logging.error(f"Ошибка при получении цен акций: {e}")
            return {}


def generate_report(input_datetime_str: str,
                    excel_path='operations.xlsx',
                    user_settings_path='user_settings.json'):
    """
       Генерирует отчет на основе операций и настроек пользователя.
    """
    input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

    df = load_operations(excel_path)
    start_date, end_date = get_date_range(input_datetime)

    settings = load_user_settings(user_settings_path)
    user_currencies = settings.get('user_currencies', [])
    user_stocks = settings.get('user_stocks', [])

    df_filtered = filter_operations_by_date(df, start_date, end_date)

    greeting = get_greeting(input_datetime)

    cards_data = aggregate_cards(df_filtered)

    top5 = top_transactions(df_filtered)

    rates = get_currency_rates(base='RUB', symbols=user_currencies)

    stock_prices = get_stock_prices(user_stocks)

    result = {
        'greeting': greeting,
        'cards': cards_data,
        'top_5_transactions': top5,
        'currency_rates': rates,
        'stock_prices': stock_prices,
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    date_str = '2020-05-20 14:30:00'
    print(generate_report(date_str))
