# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1


def fibonacci(n, m):
    """
    Функция возвращат список элементов ряда Фиббоначи с n по m
    """
    fibo = [1, 1]
    for i in range(2, m):
        fibo.append(fibo[i-2]+fibo[i-1])
    return fibo[n-1:]


print(fibonacci(1, 10))

# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()


def sort_to_max(origin_list):
    """
    Функция выполняет сортировку переданного списка по возрастанию
    Метод вставок
    """
    i = 0
    while i < len(origin_list)-1:
        i += 1
        for j in range(i):
            if origin_list[i] < origin_list[j]:
                origin_list.insert(j, origin_list.pop(i))
    return origin_list


print(sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0]))

# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.


def ff(item):
    if item >= 0:
        return True
    else:
        return False


def my_filter(filter_function, sequence):
    """
    Аналог функции filter
    """
    s = []
    for item in sequence:
        if filter_function(item):
            s.append(item)

    return s


print(my_filter(ff, [-3, 3, -2, 5, -9, -1, 0, 1]))


# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.

from math import sqrt


def is_parallelogramm(a1, a2, a3, a4):
    """
    Сумма квадратов диагоналей равна сумме квадратов сторон выпуклого четырёхугольника:
    AC**2+BD**2=AB**2+BC**2+CD**2+DA**2
    """

    def distance(point_a, point_b):
        """
        Растояние между 2мя точками
        AB = sqrt((Xb - Xa)**2 + (Yb - Ya)**2)
        """
        return sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)

    sum_diagonals = distance(a1, a3) ** 2 + distance(a2, a4) ** 2
    sum_edges = distance(a1, a2)**2 + distance(a2, a3)**2 + distance(a3, a4)**2 + distance(a4, a1)**2
    # Используем округление, чтобы не возникали проблемы с машинным нулем
    return round(sum_diagonals, 6) == round(sum_edges, 5)


print(is_parallelogramm((0, 0), (1, 2), (3, 2), (2, 0)))
print(is_parallelogramm((0, 0), (1, 2), (3, 2), (2, 1)))
