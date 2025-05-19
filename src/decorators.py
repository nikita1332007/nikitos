def log(filename=None):
    """
        Декоратор для логирования выполнения функции.

        Параметры:
        filename: str или None - имя файла для записи лога.
                   Если None, лог выводится в консоль.

        Возвращает:
        Декорированную функцию с добавленным логированием.

        """
    def decorator(func):
        def wrapper(*args, **kwargs):
            '''Эта функция принимает два аргумента и возвращает их сумму.'''
            log_output = f"{func.__name__} "
            try:
                result = func(*args, **kwargs)
                log_output += "ok"
                if filename:
                    with open(filename, 'a') as file:
                        file.write(log_output + "\n")
                else:
                    print(log_output)
                return result
            except Exception as e:
                log_output += f"error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, 'a') as file:
                        file.write(log_output + "\n")
                else:
                    print(log_output)
                raise e
        return wrapper
    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
