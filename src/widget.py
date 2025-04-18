def mask_account_card(line):
    """Функция принмает строку и маскирует у счета 2 цифры а у номера карты 6 цифр"""
    if 'Счет' in line:
      сropped_string = line[-6:]
      account_masking = сropped_string[:2]
      without_disguise = сropped_string[-4:]
      mask = "*" * len(account_masking)
      return f'Счет {mask}{without_disguise}'
    else:
        numbercard_str = str(line)
        card_type, card_number = numbercard_str.split(maxsplit=1)

        if len(card_number) <= 10:
            return f"{card_type} {card_number}"

        part_masked = "*" * (len(card_number) - 10)
        number_masked = card_number[:6] + part_masked + card_number[-4:]

        formatted_number = " ".join(number_masked[i:i + 4] for i in range(0, len(number_masked), 4))

    return f"{card_type} {formatted_number}"


print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card('MasterCard 7158300734726758'))


from datetime import datetime
def get_date(date_string):
    '''Функция принимет дату и записывает в нужный формат ДД.ММ.ГГ'''
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")


date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)
