# ДЗ по модулю Продвинутый Git
## Цель проекта
Этот проект предназначен для упрощения работы с данными, предоставляя удобные функции для анализа и визуализации. Он поможет пользователям эффективно обрабатывать большие объемы информации.
## Установка
Для установки проекта выполните следующие шаги:

1. Клонируйте репозиторий:

  git clone https://github.com/nikita1332007/nikitos

2. Перейдите в каталог проекта:
   
  cd nikitos

3. Установите зависимости:
   
  shell

  pip install -r requirements.txt

## Использование
1. Импортируйте необходимые модули:

   from nikitos import filter_by_state или sort_by_date

2. Пример использования функции:

Функция filterbystate

Эта функция фильтрует список словарей по значению ключа 'state':

def filter_by_state(dictionaries, state='EXECUTED'):
    result = []
    for item in dictionaries:
        if item.get('state') == state:
            result.append(item)
    return result


print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))  # [{'id': 41428829, 'state': 'EXECUTED', ...}, {'id': 939719570, 'state': 'EXECUTED', ...}]

Функция sortbydate

Эта функция сортирует список словарей по значению ключа 'date':

def sort_by_date(glossary, reverse=True):
    return sorted(glossary, key=lambda x: x['date'], reverse=reverse)


print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))  # Список, отсортированный по дате
