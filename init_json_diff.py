#!/usr/bin/env python3


#====================================================================================
# Назначение: Скрипт для детального сравнения двух JSON-файлов и редактирования JSON.
# Автор: Hypnodancer
# Дата создания: 30-12-2025
# Версия: 1.1
#====================================================================================

#------------------------------------------------------------------------------------
# Применение
#------------------------------------------------------------------------------------
#
# Есть два назначения для скрипта
# 1) init_json_diff.py <первый файл.JSON> <второй файл.json> -- разобрать JSON на структуру из папок и файлов (поля JSON)
# 2) make_json.py <1 или 2> -- собрать новый исправленный JSON первой или второй версии
#
#------------------------------------------------------------------------------------


import sys
import json
from itertools import count


def print_json(json_object):
    numbers = count(1)
    if type(json_object) == dict:
        print(f'словарь-{next(numbers)}')
        for key, val in json_object.items():
            print(f'key == {key}')
            if type(val) in (list, dict):
                print_json(val)
            else:
                print(f'"{val}"')
    else:
        print(f'список-{next(numbers)}')
        for val in json_object:
            if type(val) in (list, dict):
                print_json(val)
            else:
                print(f'"{val}"')

# Получаю аргументы скрипта
args = sys.argv[1:]
if len(args) != 2:
    sys.exit("В команду нужно передать два аргумента!!!\nАварийное завершение программы")

one, two = args

try:
    # Открываю два сравниваемых файла JSON
    with open(one) as first_file, open(two) as second_file:
        # Получаю JSON в формате python
        one = json.load(first_file)
        two = json.load(second_file)
except Exception as err:
    sys.exit(f"Неверные типы переданных файлов:\n{err}")


print_json(one)

