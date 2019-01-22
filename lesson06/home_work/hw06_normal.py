# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе
from random import randint


class School:
    def __init__(self, name):
        self.__name = name
        self.__classes = []
        self.__teachers = []

    def add_class(self, new_class):
        self.__classes.append(new_class)

    def get_classes(self):
        return self.__classes

    def print_classes(self):
        for i, cl in enumerate(self.get_classes()):
            print(f"{i+1}. {cl.get_name()}")

    def add_teacher(self, teacher):
        self.__teachers.append(teacher)

    def get_teachers(self):
        return self.__teachers

    def get_teachers(self, subj):
        t = []
        for item in self.__teachers:
            if item.get_subject() == subj:
                t.append(item)
        return t


class Human:
    def __init__(self, F, I, O):
        self.__F = F
        self.__I = I
        self.__O = O

    def get_fio(self):
        return self.__F, self.__I, self.__O

    def print_fio(self):
        print(f"{self.__F} {self.__I} {self.__O}")


class Teacher(Human):
    def __init__(self, F, I, O, subject):
        super().__init__(F, I, O)
        self.__subject = subject

    def get_subject(self):
        return self.__subject


class Parent(Human):
    def __init__(self, F, I, O):
        super().__init__(F, I, O)


class Pupil(Human):
    def __init__(self, F, I, O):
        super().__init__(F, I, O)

    def add_mother(self, mother):
        self.__mother = mother

    def add_father(self, father):
        self.__father = father

    def get_parents(self):
        return self.__father, self.__mother

    def print_parents(self):
        f = self.get_parents()[0].get_fio()
        m = self.get_parents()[1].get_fio()
        print(f"Отец: {f[0]} {f[1]} {f[2]}. Мать: {m[0]} {m[1]} {m[2]}")


class Class:
    def __init__(self, name):
        self.__name = name
        self.__pupils = []
        self.__teachers = []

    def add_pupil(self, pupil):
        self.__pupils.append(pupil)

    def add_teacher(self, teacher):
        self.__teachers.append(teacher)

    def get_name(self):
        return self.__name

    def get_pupils(self):
        return self.__pupils

    def print_pupils(self):
        print(f"-------- Состав: {self.get_name()} --------")
        for i, pupil in enumerate(self.get_pupils()):
            print(f"{i+1} {pupil.get_fio()[0]} {pupil.get_fio()[1]} {pupil.get_fio()[2]}")

    def get_teachers(self):
        return self.__teachers

    def print_teachers(self):
        print(f"-------- Учителя класса: {self.get_name()} --------")
        for i, teacher in enumerate(self.get_teachers()):
            print(f"{i+1} {teacher.get_fio()[0]} {teacher.get_fio()[1]} {teacher.get_fio()[2]} ({teacher.get_subject()})")

    def get_subjects(self):
        subj = []
        for teacher in self.get_teachers():
            subj.append(teacher.get_subject())
        return subj

    def print_subjects(self):
        print(f"-------- Предметы в классе: {self.get_name()} --------")
        for i, subj in enumerate(self.get_subjects()):
            print(f"{i + 1} {subj}")


def print_menu():
    print("=================================================================")
    print("0. Выход")
    print("1. Получить полный список всех классов школы")
    print("2. Получить список всех учеников в указанном классе")
    print("3. Получить список всех предметов указанного ученика")
    print("4. Узнать ФИО родителей указанного ученика")
    print("5. Получить список всех Учителей, преподающих в указанном классе")
    print("=================================================================")

def cmd_halt(s):
    return True

def cmd_print_classes(s):
    s.print_classes()
    return False

def cmd_print_pupils(s):
    try:
        n = int(input("Введите порядковый номер класса: "))
    except:
        print("Ошибка ввода, придется начинать сначала.")
    if 1 <= n <= len(s.get_classes())+1:
        s.get_classes()[n-1].print_pupils()
    else:
        print("Такого класса нет")
    return False

def cmd_print_subjects(s):
    try:
        n = int(input("Введите порядковый номер класса: "))
    except:
        print("Ошибка ввода, придется начинать сначала.")
    if 1 <= n <= len(s.get_classes())+1:
        s.get_classes()[n-1].print_subjects()
    else:
        print("Такого ученика в классе нет")
    return False

def cmd_print_parents(s):
    try:
        n = int(input("Введите порядковый номер класса: "))
    except:
        print("Ошибка ввода, придется начинать сначала.")
    if not (1 <= n <= len(s.get_classes())+1):
        print("Такого класса нет")
        return False
    try:
        m = int(input("Введите порядковый номер ученика: "))
    except:
        print("Ошибка ввода, придется начинать сначала.")
    if 1 <= m <= len(s.get_classes()[n].get_pupils()) + 1:
        s.get_classes()[n - 1].get_pupils()[m - 1].print_parents()
    else:
        print("Такого ученика в классе нет")

    return False

def cmd_print_teachers(s):
    try:
        n = int(input("Введите порядковый номер класса: "))
    except:
        print("Ошибка ввода, придется начинать сначала.")
    if 1 <= n <= len(s.get_classes())+1:
        s.get_classes()[n-1].print_teachers()
    else:
        print("Такого класса нет")
    return False


menu = {0: cmd_halt,
        1: cmd_print_classes,
        2: cmd_print_pupils,
        3: cmd_print_subjects,
        4: cmd_print_parents,
        5: cmd_print_teachers}
T_CNT = 40  # количество учителей (неограниченно)
C_CNT = 5   # количеств классов (школа расчитана на 50 классов :) )
P_CNT = 5   # количество учеников в классе (неограниченно)

# Подготовленные данные
fl = [("Иванов", "Иванова"), ("Сидоров", "Сидорова"), ("Петров", "Петрова"),
      ("Смирнов", "Смирнова"), ("Яковлев", "Яковлева"), ("Медведев", "Медведева"),
      ("Кузнецов", "Кузнецова"), ("Волков", "Волкова"), ("Зайцев", "Зайцева"),
      ("Васин", "Васина"), ("Ильин", "Ильина"), ("Губкин", "Губкина")]
il = [("Андрей", "Анастасия"), ("Евгений", "Евгения"), ("Александр", "Александра"),
      ("Семен", "Наталья"), ("Анатлоий", "Елена"), ("Роман", "Мария"),
      ("Федор", "Светлана"), ("Петр", "Екатерина"), ("Дмитрий", "Ирина")]
ol = [("Андреевич", "Андреевна"), ("Евгеньевич", "Евгеньевна"), ("Александрович", "Александровна"),
      ("Семенович", "Семеновна"), ("Анатольевич", "Анатольевна"), ("Романович", "Романовна"),
      ("Федорович", "Федоровна"), ("Петрович", "Петровна"), ("Дмитриевич", "Дмитриевна")]
subjects = ["Математика", "Физика", "Химия", "Русский язык", "Физкультура",
            "Английский язык", "Биология", "География", "ИЗО", "ОБЖ"]

# Создаем нашу школу
school = School("Школа №123")

# нанимаем учителей
for i in range(T_CNT):
    sex = randint(0, 1)  # генерируем пол ученика
    s = subjects[randint(0, len(subjects) - 1)]
    t = Teacher(fl[randint(0, len(fl) - 1)][sex], il[randint(0, len(il) - 1)][sex], ol[randint(0, len(ol) - 1)][sex], s)
    school.add_teacher(t)

# создаем классы
for i in range(C_CNT):
    c = Class(str(i % 10 + 1)+"АБВГД"[i // 10])
    school.add_class(c)
    # наполняем классы учениками
    for j in range(P_CNT):
        sex = randint(0, 1)  # генерируем пол ученика
        f_num = randint(0, len(fl) - 1)
        i_num = randint(0, len(il) - 1)
        o_num = randint(0, len(ol) - 1)
        p = Pupil(fl[f_num][sex], il[i_num][sex], ol[o_num][sex])
        c.add_pupil(p)
        # добавляем родителей
        f = Parent(fl[f_num][0], il[o_num][0], ol[randint(0, len(ol) - 1)][0])
        p.add_father(f)
        m = Parent(fl[f_num][1], il[randint(0, len(il) - 1)][1], ol[randint(0, len(ol) - 1)][1])
        p.add_mother(m)

    for subject in subjects:
        teachers = school.get_teachers(subject)
        c.add_teacher(teachers[randint(0, len(teachers)-1)])

halt = False
while not halt:
    print_menu()
    try:
        i = int(input("Введите номер операции: "))
        if not (0 <= i <= 5):
            continue
    except:
        print("Ошибка ввода")
    menu[i](school)


