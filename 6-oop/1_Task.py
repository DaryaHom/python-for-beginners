"""
Задание №1.
Создайте класс BankAccount, который представляет банковский счет. 
Определите в этом классе атрибуты account_number и balance, 
которые представляют номер счета и баланс. 
Через параметры конструктора передайте этим атрибутам начальные значения.
Также в классе определите метод add, который принимает некоторую сумму 
и добавляет ее на баланс счета. И определите метод withdraw, 
который принимает некоторую сумму и снимает ее с баланса. 
При этом с баланса нельзя снять больше, чем имеется. 
Если на балансе недостаточно средств, то пользователю должно выводиться соответствующее сообщение.
"""

from decimal import *

class BankAccount:
    def __init__(self, account_number: int, balance: Decimal):
        if not isinstance(account_number, int) or account_number <= 0:
            # Надо бы выбрасывать ошибку, но в задании - 
            # "пользователю должно выводиться соответствующее сообщение",
            # так что принт+return подходит больше
            print('Ошибка: номер счёта должен быть положительным целым числом')
            return
        if not isinstance(balance, Decimal):
            print('Ошибка: баланс должен быть числом.') 
            return
        if balance < 0:
            print('Ошибка: баланс должен быть положительным.')
            return
        
        self.__account_number = account_number
        self.__balance = balance # Приватные поля, деньги всё-таки

    @property
    def balance(self): 
        return self.__balance

    def add(self, amount: Decimal):
        if not isinstance(amount, Decimal):
            print('Ошибка: сумма пополнения должна быть числом.') 
            return
        if amount < 0:
            print('Ошибка: сумма пополнения должна быть положительной.')
            return
        self.__balance += amount

    def withdraw(self, amount: Decimal):
        if not isinstance(amount, Decimal):
            print('Ошибка: сумма снятия должна быть числом.')
            return
        if amount < 0:
            print('Ошибка: сумма снятия должна быть положительной.')
            return
        elif self.__balance - amount < 0:
            print('Ошибка: недостаточно средств на счёте.')
            return
        self.__balance -= amount
        

acc = BankAccount(123456, Decimal('0'))
acc.withdraw(Decimal('-200')) # Ошибка: сумма снятия должна быть положительной.
acc.withdraw(Decimal('200'))  # Ошибка: недостаточно средств на счёте.
acc.withdraw('99') # Ошибка: сумма снятия должна быть числом.
print(acc.balance) # 0

acc.add(Decimal('100_000_000'))
acc.withdraw(Decimal('99'))
print(acc.balance) # 99999901
