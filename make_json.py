#!/usr/bin/env python3


#====================================================================================
#                              Проект: Analizer_JSON
#====================================================================================
#                                2)  make_json.py
#====================================================================================
# Назначение: Скрипт для сборки JSON.
# Автор: Hypnodancer
# Дата создания: 03-01-2026
# Версия: 2.1
#====================================================================================

#------------------------------------------------------------------------------------
#                                   Применение
#------------------------------------------------------------------------------------
#
# Собрать новый исправленный JSON (для первого или второго файла)
#
#    make_json.py <1 или 2> <папка с проектом>
#
#------------------------------------------------------------------------------------


# diff -u <(diff -u 1.json 2.json | sed 1,2d) <(sed 1,2d diff.txt)


import sys
import json
import os
from pathlib import Path
# from datetime import datetime
# import subprocess



def is_diff():
    pass


def make_json(number, old_pwd):
    """Получаю новый python-объект после внесенных в проект изменений.
    После поиска изменений и возвращения результата он будет преобразован
    в JSON-объект и сохранен в новой папке"""

    # Текущая директория
    pwd = Path.cwd()


    # Проверяю существование файла
    file_dir = pwd / f'{number}.json'
    if file_dir.is_file():  # Если файл существует
        try:
            with open(file_dir) as file:
                # Получаю JSON в формате python
                obj_python = json.load(file)
        except Exception as err:
            sys.exit(f"Не удалось преобразовать {pwd}/{number}.json в python-объект")
    else: # Если файл не существует создаю пустой объект
        other = "2.json" if number == '1' else "1.json"
        try:
            with open(pwd / other) as file:
                # Получаю JSON в формате python
                obj_other = json.load(file)
                # Создаю пустой объект на основе другого файла
                obj_python = [] if type(obj_other) == list else {}
        except Exception as err:
            sys.exit(f"Не удалось преобразовать {pwd}/{other} в python-объект")


    # Если новый diff отличается от старого - возвращаю объект 
    if is_diff():
        return obj_python


    change = False  # изменения пока что не найдены
    if type(obj_python) == list:
        for i in range(len(obj_python)):
            try:
                nesting_dir = pwd / f'__{i}'
                if nesting_dir.is_dir():     # проверить существует ли вложенная папка
                    os.chdir(nesting_dir)    # перехожу во вложенную папку
                    result = make_json(number, pwd)
                    if result is not None:
                        change = True
                        obj_python[i] = result
            except Exception as e:
                sys.exit(f"Ошибка индекса для списка")
    else:   # если объект словарь
        for item in pwd.iterdir():
            if item.is_dir(): # Перебираю все папки
                os.chdir(nesting_dir) # перехожу во вложенную папку
                result = make_json(number, pwd)
                if result is not None:
                    change = True
                    obj_python[item.name] = result

    if change:
        return obj_python
    else:
        return None



    # После обработки вложенных объектов возвращаюсь в родительскую директорию (Произвольная вложенность)
    # Ничего не делаю, если это стартовая директория скрипта
    if old_pwd != pwd:
        os.chdir('..')



if __name__ == '__main__':
    # Получаю аргументы скрипта
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit("В команду нужно передать два аргумента!!!\nАварийное завершение программы")
    name_json, dir_project = args


    if name_json not in ("1", "2"):
        sys.exit("Вы должны указать номер варианта для сборки!!!\n"
        "Валидные значения: 1 или 2\n"
        "Синтаксис команды должен быть таким:\n"
        "make_json.py <1 или 2> <папка с проектом>")


    if not Path(dir_project).is_dir():
        sys.exit("Вы указали несуществующую папку для проекта!!!")



    # Перехожу в папку с проектом
    pwd = Path.cwd() / dir_project
    os.chdir(pwd)

    # Получаю python-объект для нового JSON
    obj_json = make_json(name_json, pwd)

    if obj_json is None:
        sys.exit("Проект не был изменен. Выгружать ничего не нужно!!!")

    
# функция возвращает словарь или список
# - Получает путь (текщую директорию)
# {генератор словаря} или [генератор списка]  -- наверху генератор-функция
