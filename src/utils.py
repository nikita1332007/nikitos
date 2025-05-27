import json
import logging
import os
from typing import List, Dict


log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'utils.log'))
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def load_transactions(json_path: str) -> List[Dict]:
    """
    Читает JSON файл с транзакциями.
    Если файл пуст, не найден или данные не являются списком - возвращает пустой список.
    """
    if not os.path.exists(json_path):
        logger.error(f"Файл не найден: {json_path}")
        return []

    try:
        with open(json_path, encoding='utf-8') as file:
            data = json.load(file)
        if not isinstance(data, list):
            logger.error("Данные не являются списком")
            return []
        logger.info("Транзакции успешно загружены")
        return data
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Ошибка при загрузке данных: {str(e)}")
        return []
