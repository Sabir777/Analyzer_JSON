#!/usr/bin/env python3


#====================================================================================
#                              Проект: Analizer_JSON
#====================================================================================
#                                2)  make_json.py
#====================================================================================
# Назначение: Скрипт для сборки JSON.
# Автор: Hypnodancer
# Дата создания: 07-01-2026
# Версия: 2.5
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



import sys
import json
import os
from pathlib import Path
import subprocess
from re import sub
from datetime import datetime



class DiffError(Exception):
    pass


def is_diff(number):
    """Функция для проверки наличия изменений в json-файлах проекта"""

    pwd = Path.cwd() # Текущая директория
    name1 = pwd / f"{number}.json"  # файл для сборки
    name2 = pwd / f".{number}.json" # теневая копия

    if name1.is_file() or name2.is_file():
        # Сравнивать с пустым файлом если одного из файлов не существует
        func_name = lambda value: str(value) if value.is_file() else '/dev/null'
        file1 = func_name(name1)
        file2 = func_name(name2)
        result = subprocess.run(
            ['diff', '-u', file1, file2],
            capture_output=True,
            text=True,
            check=False  # Не выбрасывать исключение при различии файлов
        )

        # returncode: 0=идентичны, 1=различаются, 2=ошибка
        res = result.returncode
        if res == 2:
            raise DiffError(f"Ошибка diff: {result.stderr.strip()}")
        elif res == 1:
            return True

    return False


def json_object_export(name):
    """Функция для экспорта json-файла в python-объект"""

    if name.is_file():  # Если файл существует возвращаю python-объект
        try:
            with open(name) as file:
                # Получаю JSON в формате python
                obj_python = json.load(file)
                return obj_python
        except Exception as err:
            sys.exit(f"Не удалось преобразовать {name} в python-объект")
    else:
        return None


def make_json(number, old_pwd):
    """Получаю новый python-объект после внесенных в проект изменений.
    После поиска изменений и возвращения результата он будет преобразован
    в JSON-объект и сохранен в новой папке"""

    # Текущая директория
    pwd = Path.cwd()

    # Получаю имена объектов
    file = pwd / f'{number}.json'
    other = pwd / ("2.json" if number == '1' else "1.json")

    # Получаю json-объекты
    file_json = json_object_export(file)
    other_json = json_object_export(other)

    # Проверяю изменения: если их нет, то ищу рекурсивно
    change = is_diff(number)
    if change and file_json is not None: # Изменения есть и объект существует
        return file_json 
    elif change and file_json is None: # Изменения есть, но объект был удален
        return '__json_file_remove__' 
    elif not change: # Если изменений нет в текущей папке, ищу их в дочерних папках
        if file_json is None: # Если json-файла не существует
            file_json = [] if type(other_json) == list else {}

            for item in pwd.iterdir():
                if item.is_dir(): # Если объект является папкой
                    os.chdir(item) # Перехожу в дочернюю папку
                    value = make_json(number, pwd)
                    if value is not None:
                        change = True
                        if type(file_json) == list:
                            if value != '__json_file_remove__':
                                file_json.append(value)
                        else:
                            if value != '__json_file_remove__':
                                file_json[item.name] = value

        else: # json-файл существует
            for item in pwd.iterdir():
                if item.is_dir(): # Если объект является папкой
                    os.chdir(item) # Перехожу в дочернюю папку
                    value = make_json(number, pwd)
                    if value is not None:
                        change = True
                        if type(file_json) == list:
                            if value != '__json_file_remove__':
                                file_json.append(value)
                            else:
                                index = int(item.name.removeprefix('__'))
                                if index < len(file_json):
                                    del file_json[index]
                        else:
                            if value != '__json_file_remove__':
                                file_json[item.name] = value
                            else:
                                # Если json-файла нет в дочерней папке удаляю ключ-значение из словаря
                                key = item.name
                                if key in file_json:
                                    del file_json[key]

        # После обработки вложенных объектов возвращаюсь в родительскую директорию (Произвольная вложенность)
        # Ничего не делаю, если это стартовая директория скрипта
        if old_pwd != pwd:
            os.chdir('..')

        # Если изменения были найдены возвращаю объект, в противном случае None
        if change:
            return file_json
        else:
            return None



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


    # Перехожу в директорию запуска скрипта
    os.chdir('..')

    # Создаю имя для папки в которой будет сохранен новый json
    pattern = r"^diff_([_\w-]+?)_\d{12}"
    # Уникальность по дате-времени создания
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    make_dir = Path.cwd() / sub(pattern, fr'make_\1_{timestamp}',dir_project)
    os.makedirs(make_dir, exist_ok=True) # Создаю папку

    # Записываю результат в файл
    with open(make_dir / f"make_{name_json}.json", 'w') as file:
        json.dump(obj_json, file, indent=2)

