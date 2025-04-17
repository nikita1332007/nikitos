def get_mask_card_number(card_number):
    """Функция принмает номер карты и маскирует цифры кроме первых 6 и последних 4"""
    cardnumber_str = str(card_number)
    if len(cardnumber_str) <= 10:
        return cardnumber_str
    masked_part = "*" * (len(cardnumber_str) - 10)
    masked_number = cardnumber_str[:6] + masked_part + cardnumber_str[-4:]

    return " ".join(masked_number[x : x + 4] for x in range(0, len(masked_number), 4))


card_number = 1234567890123456
masked_account = get_mask_card_number(card_number)
print(masked_account)


def get_mask_account(account_number):
    """Функция принмает номер счета и выводит последние 6 цифр где первые 2 цивры маскированы"""
    accountnumber_str = str(account_number)
    сroppedstring = accountnumber_str[-6:]
    for_masking = сroppedstring[:2]
    the_unmasked_part = сroppedstring[-4:]
    disguise = "*" * len(for_masking)

    return disguise + the_unmasked_part


account_number = 123456789556677
masked_account = get_mask_account(account_number)
print(masked_account)
