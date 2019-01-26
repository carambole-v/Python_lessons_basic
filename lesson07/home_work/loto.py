#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""

from random import randint


class Loto:
    """
    Главный класс реализующий игру
    """
    def __init__(self):
        self.bag = BarrelsBag()
        self.human = Human("Human")
        self.computer = Computer("Computer")


    def start(self):
        move_number = 0
        for barrel in self.bag:
            move_number += 1
            print("===================================================================================================")
            print(f"Ход {move_number}, в мешке осталось {len(self.bag)} бочонков")
            print("Выпал бочонок: ")
            barrel.print()
            print(f"Карточка игрока {self.human.name}")
            self.human.print_card()
            print(f"Карточка игрока {self.computer.name}")
            self.computer.print_card()
            if not self.human.move(barrel.number):
                print("--- GAME OVER ---")
                break
            if self.human.is_win():
                print(f"Player {self.human.name} WINS")
                break

            self.computer.move(barrel.number)
            if self.computer.is_win():
                print(f"Player {self.computer.name} WINS")
                break
        return


class BarrelsBag(list):
    """
    Класс реализующий мешок с бочонками на основе списка
    """
    def __init__(self):
        # наполняем наш мешок на старте всеми бочонками
        self.extend([Barrel(i + 1) for i in range(90)])

    def __iter__(self):
        return self

    def __next__(self):
        # вытаскиваем случайный бочонок из тех что есть в мешке
        if len(self) == 0:
            raise StopIteration
        return self.pop(randint(1, len(self)) - 1)


class Barrel:
    """
    Класс реализующий красивый бочонок
    """
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return str(self.number)

    def print(self):
        print("  ______")
        print(" (      )")
        print(" (  {:2}  )".format(self.number))
        print(" (      )")
        print("  ------")


class Card:
    """
    Класс реализующий карточку размером 3x9
    """
    def __init__(self):
        self.numbers = []
        self.rows = []
        # заполняем картоку 3 ряда по 5 цифр, цифры из разных десятков
        # всего 15 неповторяющихся чисел 1..90 и сортируем
        for i in range(3):
            print(i)
            self.rows.append([])
            for j in range(5):
                while True:
                    num = randint(1, 90)
                    if (num not in self.numbers) and (self.decade(num) not in [self.decade(k) for k in self.rows[i]]):
                        self.rows[i].append(num)
                        self.numbers.append(num)
                        break
            self.rows[i].sort()

        self.numbers.sort()

    @staticmethod
    def decade(number):
        """
        Функция определяет десяток к которому относится число
        """
        return abs(number) // 10 if abs(number) < 90 else 8

    def __contains__(self, item):
        for row in self.rows:
            for i in row:
                if item == i:
                    return True
        return False

    def cross_out(self, number):
        if number in self:
            for row in self.rows:
                if number in row:
                    index = row.index(number)
                    row[index] *= -1
            index = self.numbers.index(number)
            self.numbers[index] *= -1

    def print(self):
        print("----------------------------------------------")
        for row in self.rows:
            print_row = ["" for i in range(9)]
            for i in row:
                if i > 0:
                    print_row[self.decade(i)] = str(i)
                else:
                    print_row[self.decade(i)] = "XX"
            print("| {:2} | {:2} | {:2} | {:2} | {:2} | {:2} | {:2} | {:2} | {:2} |".format(*print_row))
            print("----------------------------------------------")


class Player:
    """
    Класс реализущий игрока
    """
    def __init__(self, name):
        self.name = name    # имя чтобы различать игроков
        self.card = Card()  # случайная карточка

    def print_card(self):
        self.card.print()

    def move(self, number):
        print(f"Ход игрока {self.name}...")

    def is_win(self):
        cnt = 0
        for item in self.card.numbers:
            if item < 0:
                cnt += 1
        return cnt == 15


class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def move(self, number):
        super().move(number)
        answer = ""
        while answer not in ['y', 'Y', 'n', 'N']:
            answer = input("Зачеркнуть цифру (y/n)? ")
        print(f"Игрок {self.name} сделал свой ход")
        if (answer.lower() == 'n') and (number in self.card):
            return False
        if (answer.lower() == 'y') and (number not in self.card):
            return False
        self.card.cross_out(number)
        return True


class Computer(Player):
    def __init__(self, name):
        super().__init__(name)

    def move(self, number):
        super().move(number)
        if number in self.card:
            self.card.cross_out(number)
        print(f"Игрок {self.name} сделал свой ход")
        return True

loto = Loto()
loto.start()