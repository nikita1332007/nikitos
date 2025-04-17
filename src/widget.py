def mask_account_card(line):
    if 'Счет' in line:
      сroppedstring = line[-6:]
      for_masking = сroppedstring[:2]
      the_unmasked_part = сroppedstring[-4:]
      disguise = "*" * len(for_masking)
      return f'Счет {disguise}{the_unmasked_part}'
    else:
        parts = line.split()
        if len(parts) < 2:
            return line
        card_type = parts[0]
        number = ''.join(filter(str.isdigit, parts[1]))
        if len(number) != 16:
            return line
    masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    return f"{card_type} {masked_number}"


print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card('MasterCard 7158300734726758'))


from datetime import datetime
def get_date(date_string):
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")


date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)



