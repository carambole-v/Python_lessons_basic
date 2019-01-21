# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.

from math import sqrt


class Triangle:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        # Координаты вершин
        self.x = (x1, x2)
        self.y = (y1, y2)
        self.z = (z1, z2)
        # Сразу вычислим длины сторон, они нам понадобятся в расчетах
        self.a = self.__distance(self.x, self.y)
        self.b = self.__distance(self.x, self.z)
        self.c = self.__distance(self.y, self.z)

    def __distance(self, x1, x2):
        """
        Растояние между 2мя точками
        """
        return sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)

    def perimeter(self):
        return self.a + self.b + self.c

    def square(self):
        """
        Площадь по формуле Герона
        """
        p = self.perimeter()/2
        return sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def height_a(self):
        """
        Высота XY
        """
        p = self.perimeter() / 2
        return 2 / self.a * sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def height_b(self):
        """
        Высота XZ
        """
        p = self.perimeter() / 2
        return 2 / self.b * sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def height_c(self):
        """
        Высота YZ
        """
        p = self.perimeter() / 2
        return 2 / self.c * sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


# Проверка на примере Пифагорова треугольника
t = Triangle(0, 0, 0, 3, 4, 0)
print(t.perimeter())
print(t.square())
print(t.height_a())
print(t.height_b())
print(t.height_c())

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.
from math import sqrt


class Trapezium:
    def __init__(self, a1, a2, b1, b2, c1, c2, d1, d2):
        # Координаты вершин
        # Допуск: вводим по часовой стрелке с левого нижнего угла
        self.a = (a1, a2)
        self.b = (b1, b2)
        self.c = (c1, c2)
        self.d = (d1, d2)

    def __distance(self, x1, x2):
        """
        Растояние между 2мя точками
        """
        return sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)

    def is_isosceles(self):
        """
        Трапеция равнобокая если диагонали равны
        """
        return self.__distance(self.a, self.c) == self.__distance(self.b, self.d)

    def get_ab(self):
        return self.__distance(self.a, self.b)

    def get_bc(self):
        return self.__distance(self.b, self.c)

    def get_cd(self):
        return self.__distance(self.c, self.d)

    def get_da(self):
        return self.__distance(self.d, self.a)

    def perimeter(self):
        # Тут все просто
        return self.get_ab() + self.get_bc() + self.get_cd() + self.get_da()

    def height(self):
        # Ужас, ужас...
        t = ( ( (self.get_da() - self.get_bc())**2 + self.get_ab()**2 - self.get_cd()**2) / (2 * (self.get_da() - self.get_bc())) )**2
        return sqrt(self.get_ab() ** 2 - t)

    def square(self):
        # полусумма оснований на высоту
        return 1/2 * (self.get_bc() + self.get_da()) * self.height()


# Проверка на простом случае
t = Trapezium(0, 0, 1, 4, 5, 4, 6, 0)
print(t.height())
print(t.square())
print(t.perimeter())
