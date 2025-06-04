from src.base import read_json_file, read_csv_file, read_xlsx_file, search_operations


def main():
    """
        Главная функция программы для работы с банковскими транзакциями.

    """
    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из JSON-файла')
    print('2. Получить информацию о транзакциях из CSV-файла')
    print('3. Получить информацию о транзакциях из XLSX-файла')

    choice = input('Пользователь: ').strip()
    reader = {
        '1': read_json_file,
        '2': read_csv_file,
        '3': read_xlsx_file
    }.get(choice)

    if reader is None:
        print('Некорректный выбор файла.')
        return

    file_path = input('Введите путь к файлу: ').strip()
    operations = reader(file_path)

    if not operations:
        print('Файл не содержит операций или пуст.')
        return

    statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        status = input('Введите статус для фильтрации: ').strip().upper()
        if status in statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            filtered_operations = [
                op for op in operations
                if isinstance(op.get('state'), str) and op['state'].upper() == status
            ]
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    if not filtered_operations:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.')
        return

    if input('Отсортировать операции по дате? Да/Нет: ').strip().lower() == 'да':
        order = input('Отсортировать по возрастанию или по убыванию? ').strip().lower()
        filtered_operations.sort(key=lambda x: x['date'], reverse=order == 'по убыванию')

    if input('Выводить только рублевые транзакции? Да/Нет: ').strip().lower() == 'да':
        filtered_operations = [
            op for op in filtered_operations
            if isinstance(op.get('amount'), str) and 'RUB;' in op['amount']
        ]

    if input('Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ').strip().lower() == 'да':
        search_term = input('Введите слово для поиска: ')
        filtered_operations = search_operations(filtered_operations, search_term)

    if not filtered_operations:
        print('Не найдено ни одной транзакции, соответствующей вашим условиям фильтрации.')
        return

    print('Распечатываю итоговый список транзакций:')
    print(f'Всего банковских операций в выборке: {len(filtered_operations)}')
    for op in filtered_operations:
        print(f"{op['date']} {op['description']}\nСчет {op.get('account', '')}\nСумма: {op.get('amount', '')}\n")


if __name__ == '__main__':
    main()
