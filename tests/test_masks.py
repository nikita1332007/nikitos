import pytest

from src.masks import get_mask_card_number, get_mask_account


card_numbers = [
    (1234567890123456, "1234 56** **** 3456"),
    (1234, "1234"),
    ("123456789012", "1234 56** 9012"),
    ("", ""),
    ("abcdefghij", "abcdefghij"),
    (12345678901234567890, "1234 56** **** **** 7890"),
    (123456789012345, "1234 56** ***2 345")
]

account_numbers = [
    (123456789012, "**9012"),
    (987654, "**7654"),
    (12, "**12"),
    ("", ""),
    (123456789, "**6789"),
    (100, "**100")
]

@pytest.mark.parametrize("input_num, expected", card_numbers)
def test_get_mask_card_number(input_num, expected):
    assert get_mask_card_number(input_num) == expected

@pytest.mark.parametrize("input_num, expected", account_numbers)
def test_get_mask_account(input_num, expected):
    assert get_mask_account(input_num) == expected