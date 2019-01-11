# Задание-1:
# Напишите функцию, округляющую полученное произвольное десятичное число
# до кол-ва знаков (кол-во знаков передается вторым аргументом).
# Округление должно происходить по математическим правилам (0.6 --> 1, 0.4 --> 0).
# Для решения задачи не используйте встроенные функции и функции из модуля math.

def my_round(number, ndigits):
    """
    Округление полученного десятичного числа до указанного количества знаков
    """
    # выполним проверку
    if (ndigits < 0):
        return

    # все что оставим загоняем в целую часть и при необходимости добавляем 1
    result = number * 10 ** ndigits

    # применяем правило округления
    if result - int(result) >= 0.5:
        result += 1
    result = int(result)

    # двигаем разряды взад
    result *= 10 ** -ndigits
    return result

print(my_round(2.1234567, 5))
print(my_round(2.1999967, 5))
print(my_round(2.9999967, 5))

# Задание-2:
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить

def lucky_ticket(ticket_number):
    if (ticket_number < 100000) or (ticket_number > 999999):
        return False
    first3 = int(ticket_number / 10**5) % 10 + int(ticket_number / 10**4) % 10 + int(ticket_number / 10**3) % 10
    last3 =  int(ticket_number / 10**2) % 10 + int(ticket_number / 10**1) % 10 + int(ticket_number / 10**0) % 10
    return first3 == last3


print(lucky_ticket(123006))
print(lucky_ticket(12321))
print(lucky_ticket(436751))
