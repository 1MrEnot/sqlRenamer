import os
from typing import List

from Common import split_string


def replace(string: str, positions: List[int]) -> str:
    """
    :param string: одна строка sql запроса, в формате (a, b, c, ... )
    :param positions: Список индексов. i-тому элементу выходной строки соответсвует positions[i] элемент входной
    :return:
    """
    res_string = string

    try:
        start_symbol, stop_symbol = '(', ')'

        start_index, stop_index = string.find(start_symbol), string.rfind(stop_symbol)

        args_part = string[start_index+1: stop_index]
        args = split_string(args_part)

        new_args = map(lambda i: args[i], positions)
        new_args_part = ', '.join(new_args)

        res_string = string.replace(args_part, new_args_part)

    except Exception:
        pass

    return res_string


if __name__ == '__main__':
    # Путь и название файла
    directory, filename = r"C:\Users\MaX\Desktop", "а.txt"
    # Массив индексов
    # positions = [0, 1, 2, 11, 12, 4, 5, 6, 18, 19, 8, 9, 10, 13, 14, 20, 15, 16, 7, 3]
    positions = [0, 3, 4, 1, 2]

    # ----------

    new_filename = f"new_{filename}"

    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
        file_rows = f.readlines()

    new_rows = map(lambda x: replace(x, positions), file_rows)

    with open(os.path.join(directory, new_filename), 'w+', encoding='utf-8') as f:
        f.writelines(new_rows)

    print(f"Done! Wrote to {os.path.join(directory, new_filename)}")

