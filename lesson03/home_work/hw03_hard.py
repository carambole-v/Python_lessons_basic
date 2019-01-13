# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3

def fraction(str):
    """
    Представляем дробь в удобном виде
    """
    if str.find(" ") != -1:
        # введена дробь с целой частью
        integer = int(str.split(" ")[0])
        numerator = int(str.split(" ")[1].split("/")[0])
        denominator = int(str.split(" ")[1].split("/")[1])
    elif str.find("/") != -1:
        # введена дробь без целой части
        integer = 0
        numerator = int(str.split("/")[0])
        denominator = int(str.split("/")[1])
    else:
        # введено только целое
        integer = int(str)
        numerator = 0
        denominator = 1  # на ноль делить нельзя. хотя, какая разница
    # преобразуем в неправильную дробь
    if integer < 0:
        numerator += -1*denominator*integer
        numerator *= -1
    else:
        numerator += denominator*integer
    return numerator, denominator


def gcd(a, b):
    """
    НОД двух чисел, чтобы сократить дробь
    """
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a

    return a + b


def fsum(f1, f2):
    """
    Сумма дробей
    """
    numerator = f1[0]*f2[1]+f2[0]*f1[1]
    denominator = f1[1]*f2[1]
    integer = numerator // denominator
    if integer < 0:
        # фиксим жесть: -2//8 = -1 (((
        integer +=1
    numerator -= integer*denominator
    d = gcd(abs(numerator), abs(denominator))
    return integer, numerator//d, denominator//d


def fdiff(f1, f2):
    """
    Разность дробей
    """
    numerator = f1[0]*f2[1]-f2[0]*f1[1]
    denominator = f1[1]*f2[1]
    integer = numerator // denominator
    if integer < 0:
        # фиксим жесть: -2//8 = -1 (((
        integer +=1
    numerator -= integer*denominator
    d = gcd(abs(numerator), abs(denominator))
    return integer, numerator//d, denominator//d


s = input("Введите выражение: ")

if s.find(" + ") != -1:
    res = fsum(fraction(s.split(" + ")[0]), fraction(s.split(" + ")[1]))
elif s.find(" - ") != -1:
    res = fdiff(fraction(s.split(" - ")[0]), fraction(s.split(" - ")[1]))
else:
    failed = True
    print("Введена какая-то ерунда")

if not failed:
    if (res[1] != 0) and (res[0] != 0):
        print(f"Результат выражения: {res[0]} {res[1]}/{res[2]}")
    elif (res[1] != 0) and (res[0] == 0):
        print(f"Результат выражения: {res[1]}/{res[2]}")
    else:
        print(f"Результат выражения: {res[0]}")

# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"
import os

path = os.path.join('data', 'workers')
f_workers = open(path, 'r', encoding='UTF-8')
workers = f_workers.readlines()
f_workers.close()

path = os.path.join('data', 'hours_of')
f_hours = open(path, 'r', encoding='UTF-8')
hours = f_hours.readlines()
f_hours.close()

# загоним ведомость в словарь
sheet = {}

i = 0
while i < len(workers) - 1:
    i += 1
    worker = " ".join(workers[i].split())
    worker = worker.split(" ")
    sheet[worker[0] + " " + worker[1]] = {"Зарплата": int(worker[2]), "Норма": int(worker[4])}

i = 0
while i < len(hours) - 1:
    i += 1
    hour = " ".join(hours[i].split())
    hour = hour.split(" ")
    sheet[hour[0] + " " + hour[1]]["Отработано"] = int(hour[2])

for k in sheet:
    print(f"Работнику {k} выплатить {sheet[k]['Зарплата'] * sheet[k]['Отработано'] / sheet[k]['Норма']}")

# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))

import os

path = os.path.join('data', 'fruits.txt')
f = open(path, 'r', encoding='UTF-8')
fruits = {}
for fruit in f.readlines():
    if fruit == "\n":
        continue
    if fruit[0] in fruits.keys():
        fruits[fruit[0]] += [fruit]
    else:
        fruits[fruit[0]] = [fruit]
f.close()

for key in fruits:
    path = os.path.join('data', f'fruits_{key}.txt')
    f = open(path, 'w', encoding='UTF-8')
    f.writelines(fruits[key])
    f.close()
