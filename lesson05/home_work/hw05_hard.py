# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.


import os
import sys


def print_help():
    print("help - получение справки")
    print("cp <file_name> - создает копию указанного файла")
    print("rm <file_name> - удаляет указанный файл")
    print("cd <full_path or relative_path> - меняет текущую директорию на указанную")
    print("ls - отображение полного пути текущей директории")


def cmd_cp(source_fn):
    dest_fn = source_fn + ".cpy"
    try:
        source = open(source_fn, "r", encoding="UTF-8")
        content = source.readlines()
    except Exception as e:
        print(f"Возникла ошибка при чтении из файла {source_fn}: {e}")
    finally:
        source.close()

    try:
        dest = open(dest_fn, "w", encoding="UTF-8")
        dest.writelines(content)
    except Exception as e:
        print(f"Возникла ошибка при записи в файл {dest_fn}: {e}")
    finally:
        dest.close()


def cmd_rm(filename):
    if input(f"Будет удален файл {filename}. Для подтверждения операции введите yes: ") != "yes":
        return
    try:
        os.remove(filename)
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    return


def cmd_cd(path):
    try:
        os.chdir(path)
        print(f"Текущая директория: {os.getcwd()}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return


def cmd_ls():
    print(f"Текущая директория: {os.getcwd()}")
    return


do = {"help": print_help,
      "cp": cmd_cp,
      "rm": cmd_rm,
      "cd": cmd_cd,
      "ls": cmd_ls}

try:
    key = sys.argv[1]
except IndexError:
    key = None
    print_help()

if key != "ls":
    try:
        param = sys.argv[2]
    except IndexError:
        param = None
else:
    param = None

if key:
    if do.get(key):
        do[key](param) if param else do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")
