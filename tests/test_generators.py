import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def transactions_with_missing_code():
    return [
        {
            'id': 1,
            'operationAmount': {
                'amount': '1000',
                'currency': {'name': 'USD'}
            }
        },
        {
            'id': 2,
            'operationAmount': {
                'amount': '2000',
                'currency': {'name': 'RUB'}
            }
        }
    ]


@pytest.fixture
def transactions_data():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"code": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {"amount": "79114.93", "currency": {"code": "USD"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {"amount": "43318.34", "currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "operationAmount": {"amount": "56883.54", "currency": {"code": "USD"}},
            "description": "Перевод с карты на карту"
        }
    ]


def test_filter_by_currency_with_usd(sample_transactions):
    filtered_transactions = list(filter_by_currency(sample_transactions, 'USD'))
    assert len(filtered_transactions) == 3
    assert all(t['operationAmount']['currency']['code'] == 'USD' for t in filtered_transactions)


def test_filter_by_currency_with_rub(sample_transactions):
    filtered_transactions = list(filter_by_currency(sample_transactions, 'RUB'))
    assert len(filtered_transactions) == 2
    assert all(t['operationAmount']['currency']['code'] == 'RUB' for t in filtered_transactions)


def test_filter_by_currency_no_transactions():
    filtered_transactions = list(filter_by_currency([], 'USD'))
    assert filtered_transactions == []


def test_filter_by_currency_non_existent_currency(sample_transactions):
    filtered_transactions = list(filter_by_currency(sample_transactions, 'EUR'))
    assert filtered_transactions == []


def test_filter_by_currency_with_missing_code_key(transactions_with_missing_code):
    filtered_transactions = list(filter_by_currency(transactions_with_missing_code, 'USD'))
    assert filtered_transactions == []


def test_transaction_descriptions(transactions_data):
    descriptions = list(transaction_descriptions(transactions_data))
    assert len(descriptions) == 4
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]


def test_transaction_descriptions_empty():
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


def test_transaction_descriptions_one_transaction():
    single_transaction = [{
        "id": 1,
        "state": "EXECUTED",
        "operationAmount": {"amount": "1000.00", "currency": {"code": "USD"}},
        "description": "Тестовая транзакция"
    }]
    descriptions = list(transaction_descriptions(single_transaction))
    assert len(descriptions) == 1
    assert descriptions[0] == "Тестовая транзакция"


def test_transaction_descriptions_different_descriptions():
    transactions = [
        {"description": "Транзакция 1"},
        {"description": "Транзакция 2"}
    ]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Транзакция 1", "Транзакция 2"]


@pytest.fixture
def card_generator():
    return card_number_generator


def test_card_number_generator(card_generator):
    expected_output = ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert list(card_generator(0, 3)) == expected_output

    expected_output = ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001", "0000 0000 0001 0002"]
    assert list(card_generator(9999, 10002))[:4] == expected_output

    assert list(card_generator(0, 0)) == ["0000 0000 0000 0000"]
    assert list(card_generator(9999, 9999)) == ["0000 0000 0000 9999"]
    assert list(card_generator(5, 5)) == ["0000 0000 0000 0005"]


if __name__ == "__main__":
    pytest.main()
