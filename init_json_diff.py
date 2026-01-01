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
from datetime import datetime


def print_json(json_object, name_json, old_pwd):
    """Функция для создания структуры из файлов и папок
    в соответствии со структурой JSON-файла. Для каждого
    вложенного объекта будет создаваться отдельная папка"""

    # Определяю текущую директорию
    pwd = Path.cwd()

    # Создаю файл JSON в текущей директории для данного объекта
    with open(f'{name_json}.json', 'w') as file:
        json.dump(json_object, file, indent=2)

    # Каждый объект JSON - это итерируемый объект
    # Если его элемент - это вложенный объект, то он обрабатывается рекурсивно
    if type(json_object) == list:
        for index, val in enumerate(json_object):
            if type(val) in (list, dict):
                new_dir = pwd / f'__{index}'
                os.makedirs(new_dir, exist_ok=True) # Создаю номерную папку для списка
                os.chdir(new_dir) # Перехожу в новую папку
                print_json(val, name_json, pwd)

    else: # если json_object это dict, то каждый элемент сохраняю в папке с именем ключа
        for key, val in json_object.items():
            if type(val) in (list, dict):
                new_dir = pwd / f'{key}'
                os.makedirs(new_dir, exist_ok=True) # Создаю папку с именем ключа
                os.chdir(new_dir) # Перехожу в новую папку
                print_json(val, name_json, pwd)


    # После обработки вложенных объктов возвращаюсь в родительскую директорию (Произвольная вложенность)
    # Ничего не делаю, если это стартовая директория скрипта
    if old_pwd != pwd:
        os.chdir('..')



if __name__ == '__main__':
    # Получаю аргументы скрипта
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit("В команду нужно передать два аргумента!!!\nАварийное завершение программы")
    first_name, second_name = args

    try:
        # Открываю два сравниваемых файла JSON
        with open(first_name) as first_file, open(second_name) as second_file:
            # Получаю JSON в формате python
            one = json.load(first_file)
            two = json.load(second_file)
    except Exception as err:
        sys.exit(f"Неверные типы переданных файлов:\n{err}")


    
    # Удаляю суффикс .json из имени
    first_name = first_name.removesuffix(".json")
    second_name = second_name.removesuffix(".json")
    # Создаю папку с проектом (уникальность по именам и дате-времени создания)
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    new_dir = f'diff_{first_name}__{second_name}_{timestamp}'
    os.makedirs(new_dir, exist_ok=True) # Создаю папку
    os.chdir(new_dir) # Перехожу в новую папку
    pwd = Path.cwd() # Текущая директория скрипта

    # Передаю в функцию объект JSON, номер JSON и текущую директорию
    print_json(one, 1, pwd)
    print_json(two, 2, pwd)

