from datetime import datetime


def mask_account_card(line):
    """Функция принмает строку и маскирует у счета 2 цифры а у номера карты 6 цифр"""
    if 'Счет' in line:
        сropped_string = line[-6:]
        account_masking = сropped_string[:2]
        without_disguise = сropped_string[-4:]
        mask = "*" * len(account_masking)
        return f'Счет {mask}{without_disguise}'
    else:
        card_number_str = str(line)

        card_type, number_card = card_number_str.rsplit(' ', 1)

        if len(number_card) <= 10:
            return f"{card_type} {number_card}"

        part_masked = "*" * (len(number_card) - 10)
        number_masked = number_card[:6] + part_masked + number_card[-4:]

        formatted_masked_number = " ".join(number_masked[i:i + 4] for i in range(0, len(number_masked), 4))

        return f"{card_type} {formatted_masked_number}"


print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card('MasterCard 7158300734726758'))
print(mask_account_card('Счет 35383033474447895560'))
print(mask_account_card('Visa Classic 6831982476737658'))
print(mask_account_card('Visa Platinum 8990922113665229'))
print(mask_account_card('Visa Gold 5999414228426353'))
print(mask_account_card('Счет 73654108430135874305'))


def get_date(date_string):
    '''Функция принимет дату и записывает в нужный формат ДД.ММ.ГГ'''
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")


date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)
