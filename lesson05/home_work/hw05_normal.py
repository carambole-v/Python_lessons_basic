# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py
import os
import sys


def print_menu(menu):
    for item in menu:
        print(item)
    print()
    return


def cmd_cd():
    dirname = input("Введите имя директории: ")
    try:
        os.chdir(dirname)
        print(f"Текущая директория {os.getcwd()}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return False


def cmd_list(dirname=None):
    print(f"Листинг директории: ")
    for item in os.listdir():
        print(item)
    return False


def cmd_delete(dirname=None):
    dirname = input("Введите имя директории для удаления: ")
    try:
        os.rmdir(dirname)
        print(f"Удалено")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return False


def cmd_create(dirname=None):
    dirname = input("Введите имя новой директории: ")
    try:
        os.mkdir(dirname)
        print(f"Создано")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return False


def cmd_halt():
    return True


halt = False
menu = {"0. Выход": cmd_halt,
        "1. Перейти в папку": cmd_cd,
        "2. Просмотреть содержимое текущей папки": cmd_list,
        "3. Удалить папку": cmd_delete,
        "4. Создать папку": cmd_create}

while not halt:
    print_menu(menu)
    try:
        n = int(input("Введите операцию: "))
    except Exception as e:
        print("Вводите правильно! Нужно число от 0 до 4")
        print()
        continue
    if (n < 0) or (n >= len(menu)):
        print("Недопустимая операция")
        print()
        continue
    halt = menu[list(menu)[n]]()
    print()
