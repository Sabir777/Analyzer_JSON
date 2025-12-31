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
import os
from pathlib import Path
# from itertools import count


# def print_json(json_object):
    # numbers = count(1)
    # if type(json_object) == dict:
        # print(f'словарь-{next(numbers)}')
        # for key, val in json_object.items():
            # print(f'key == {key}')
            # if type(val) in (list, dict):
                # print_json(val)
            # else:
                # print(f'"{val}"')
    # else:
        # print(f'список-{next(numbers)}')
        # for val in json_object:
            # if type(val) in (list, dict):
                # print_json(val)
            # else:
                # print(f'"{val}"')



def print_json(json_object, n_json, old_pwd):
    """Функция для создания структуры из файлов и папок
    в соответствии со структурой JSON-файла. Для каждого
    вложенного объекта будет создаваться отдельная папка"""

    # Каждый объект JSON - это итерируемый объект
    # Если его элемент - это вложенный объект, то он обрабатывается рекурсивно

    # Создаю файл JSON в текущей директории для данного объекта

    # Определяю текущую директорию

    for index, val in enumerate(json_object):
        if type(val) in (list, dict):
        match val:
            case list():
                old_pwd = Path.cwd()
                new_dir = old_pwd / f'__{index}'
                os.makedirs(new_dir, exist_ok=True) # Создаю папку для списка
                os.chdir(new_dir) # Перехожу в новую папку
                print_json(val, n_json, old_pwd)

    if old_pwd != Path.cwd():
        os.chdir('..') # Возвращаюсь в родительскую директорию




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



if __name__ == '__main__':
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


    _pwd = Path.cwd() # Текущая директория скрипта
    print_json(one, 1, _pwd) # Передаю в функцию номер JSON и текущую директорию

