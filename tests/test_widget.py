import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date


@pytest.fixture
def account_data():
    return [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92 ** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41 ** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Некорректный ввод", "Некорректный ввод"),
    ]


@pytest.mark.parametrize("account_str, expected", [
    ("Счет 64686473678894779589", "Счет **9589"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет 35383033474447895560", "Счет **5560"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Некорректный ввод", "Некорректный ввод")
])
def test_mask_account_card(account_str, expected):

    assert mask_account_card(account_str) == expected


@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2022-12-31T14:59:59", "31.12.2022"),
    ("2000-01-01", "01.01.2000"),
    ("Некорректная строка", pytest.mark.xfail(raises=ValueError)),
    ("", pytest.mark.xfail(raises=ValueError)),
    (None, pytest.mark.xfail(raises=ValueError)),
])
def get_date(date_str):
    if not isinstance(date_str, str):
        raise ValueError("Input must be a string")
    try:
        return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date format")
