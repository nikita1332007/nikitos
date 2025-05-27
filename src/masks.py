import logging
import os

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'masks.log'), encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number):
    """Маскировка номера карты"""
    cardnumber_str = str(card_number)
    if len(cardnumber_str) <= 10:
        logger.error("Номер карты недостаточной длины.")
        return cardnumber_str
    masked_part = "*" * (len(cardnumber_str) - 10)
    masked_number = cardnumber_str[:6] + masked_part + cardnumber_str[-4:]

    logger.info("Номер карты успешно замаскирован.")
    return " ".join(masked_number[x: x + 4] for x in range(0, len(masked_number), 4))


def get_mask_account(account_number):
    """Маскировка номера счета"""
    accountnumber_str = str(account_number)
    if len(accountnumber_str) < 6:
        logger.error("Номер счета недостаточной длины.")
        return accountnumber_str
    cropped_string = accountnumber_str[-6:]
    disguise = "*" * 2
    masked_account = disguise + cropped_string[-4:]

    logger.info("Номер счета успешно замаскирован.")
    return masked_account


card_number = 1234567890123456
masked_card = get_mask_card_number(card_number)
print(masked_card)

account_number = 123456789556677
masked_account = get_mask_account(account_number)
print(masked_account)
