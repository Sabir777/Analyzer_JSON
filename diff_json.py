#!/usr/bin/env python3


#====================================================================================
#                              Проект: Analizer_JSON
#====================================================================================
#                                1)  diff_json.py
#====================================================================================
# Назначение: Скрипт для детального сравнения двух JSON-файлов и редактирования JSON.
# Автор: Hypnodancer
# Дата создания: 03-01-2026
# Версия: 2.1
#====================================================================================

#------------------------------------------------------------------------------------
#                                   Аннотация
#------------------------------------------------------------------------------------
#
#                       Проект состоит из двух частей:
#
# 1) Разобрать JSON на составляющие части
#
#    diff_json.py <первый файл.JSON> <второй файл.json>
#
#   - в папках где есть 1.json и 2.json будет создан файл diff.txt если между файлами
# есть отличия (отличия будут даже если существует только один файл)
#
# 2) Собрать новый исправленный JSON (для первого или второго файла)
#
#    make_json.py <1 или 2> <папка с проектом>
#
#------------------------------------------------------------------------------------


import sys
import json
import os
from pathlib import Path
from datetime import datetime
import subprocess


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


    # После обработки вложенных объектов возвращаюсь в родительскую директорию (Произвольная вложенность)
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


    # Сравниваю diff -u 1.json 2.json во всех папках включая вложенные
    for dirpath, _, files in os.walk(pwd):
        current_dir = Path(dirpath)
        
        # Проверяю наличие 1.json и 2.json
        if '1.json' in files or '2.json' in files:
            # Если одного из файлов не существует, то сравнивать с пустым файлом
            f_file = lambda name: str(current_dir / name) if name in files else '/dev/null'
            file1 = f_file('1.json')
            file2 = f_file('2.json')
            diff_file = current_dir / 'diff.txt'
            
            try:
                result = subprocess.run(
                    ['diff', '-u', file1, file2],
                    capture_output=True,
                    text=True,
                    check=False  # Не выбрасывать исключение при различии файлов
                )
                

                # Сохраняю различия в файл diff.txt если вывод НЕ пустой
                if result.stdout:
                    diff_file.write_text(result.stdout)
                
            except Exception as e:
                print(f"  ✗ Ошибка: {e}")
