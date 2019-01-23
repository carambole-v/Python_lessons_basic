# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла
import re
import os


class Worker:
    def __init__(self, line):
        # удаляем множественные пробелы и делим по оставшимся
        s = re.sub(r'\s+', ' ', line)
        self.name = s.split(" ")[0]
        self.surname = s.split(" ")[1]
        self.salary = int(s.split(" ")[2])
        self.position = s.split(" ")[3]
        self.rate = int(s.split(" ")[4])
        self.fact = 0

    def print(self):
        print(f"{self.name} {self.surname} должен получить {self.get_total_salary()}")

    def set_fact(self, fact):
        self.fact = fact

    def get_total_salary(self):
        if self.fact < self.rate:
            return self.salary * self.fact / self.rate
        else:
            return self.salary + 2 * self.salary * (self.fact-self.rate) / self.rate


workers = []
try:
    path = os.path.join('data', 'workers')
    fw = open(path, 'r', encoding='UTF-8')
    for item in fw.readlines()[1:]:
        workers.append(Worker(item))
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    fw.close()

try:
    path = os.path.join('data', 'hours_of')
    fh = open(path, 'r', encoding='UTF-8')
    for line in fh.readlines()[1:]:
        s = re.sub(r'\s+', ' ', line)
        for worker in workers:
            if (worker.name == s.split()[0]) and (worker.surname == s.split()[1]):
                worker.set_fact(int(s.split()[2]))
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    fh.close()

for worker in workers:
    worker.print()
