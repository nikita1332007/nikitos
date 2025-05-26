from src.external_api import convert_to_rub

if __name__ == "__main__":

    transactions = [
        {'amount': 100, 'currency': 'USD'},
        {'amount': 200, 'currency': 'EUR'},
        {'amount': 3000, 'currency': 'RUB'},
        {'amount': 150, 'currency': 'GBP'},
        {'amount': 500, 'currency': ''},
    ]

    for tx in transactions:
        rub_amount = convert_to_rub(tx)
        print(f"Исходный: {tx['amount']} {tx.get('currency', 'RUB')}, в RUB: {rub_amount}")
