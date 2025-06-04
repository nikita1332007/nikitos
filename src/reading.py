import pandas as pd


def read_csv(file_path):
    """
        Читает CSV файл и возвращает данные в виде списка словарей.

    """
    csv_data = pd.read_csv(file_path)
    return csv_data.to_dict(orient='records')


csv_result = read_csv(r'C:\Users\Nikita\PycharmProjects\transactions.csv')

print(csv_result)


def read_excel(file_path):
    """
        Читает Excel файл и возвращает данные в виде списка словарей.
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient='records')


xlsx_result = read_excel(r'C:\Users\Nikita\PycharmProjects\transactions_excel.xlsx')
print(xlsx_result)
