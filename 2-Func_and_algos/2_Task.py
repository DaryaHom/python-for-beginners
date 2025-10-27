### Задача №2. Программа для мини-банка

# Реализуйте программу, состоящую из трёх функций:

# 1. `greet_client(first_name, last_name)` — выводит приветствие по имени и фамилии в зависимости от времени суток в Москве:  
#    - 6:00–11:59 → «Доброе утро»  
#    - 12:00–17:59 → «Добрый день»  
#    - 18:00–23:59 → «Добрый вечер»  
#    - 0:00–5:59 → «Доброй ночи»  
#    Пример: `greet_client("Анна", "Петрова")` → при времени 14:30 выводит: `Добрый день, Анна Петрова!`

# 2. `deposit(balance, amount)` — пополняет счёт на `amount`, если сумма > 0. Иначе выводит ошибку и не меняет баланс. Возвращает новый (или старый) баланс.  
#    Пример 1: `deposit(1000, 500)` → возвращает `1500`  
#    Пример 2: `deposit(1000, -200)` → выводит `Ошибка: сумма пополнения должна быть положительной.` и возвращает `1000`

# 3. `withdraw(balance, amount)` — снимает `amount`, если сумма > 0 и ≤ баланса. Иначе — ошибка. Возвращает новый (или старый) баланс.  
#    Пример 1: `withdraw(1000, 300)` → возвращает `700`  
#    Пример 2: `withdraw(1000, 1500)` → выводит `Ошибка: недостаточно средств на счёте.` и возвращает `1000`  
#    Пример 3: `withdraw(1000, -100)` → выводит `Ошибка: сумма снятия должна быть положительной.` и возвращает `1000`

# Требования:  
# - Все функции реализуются в одном файле.  
# - В `greet_client` используй `datetime` с часовым поясом `Europe/Moscow`.  
# - Ошибки выводятся через `print()`, но функции всегда возвращают число (баланс).

from datetime import datetime, time
import pytz                           # pip install pytz==2025.2

_MORNING_START = time.fromisoformat('06:00')
_MORNING_END = time.fromisoformat('11:59')

_DAY_START = time.fromisoformat('12:00')
_DAY_END = time.fromisoformat('17:59')

_EVENING_START = time.fromisoformat('18:00')
_EVENING_END = time.fromisoformat('23:59')

def greet_client(first_name, last_name):
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow')).time()

    greet = 'Доброй ночи'
    if _MORNING_START <= moscow_time <= _MORNING_END:
        greet = 'Доброе утро' 
    elif _DAY_START <= moscow_time <= _DAY_END:
        greet = 'Добрый день'
    elif _EVENING_START <= moscow_time <= _EVENING_END:
        greet = 'Добрый вечер'

    print(f'{greet}, {first_name} {last_name}!')
    
def deposit(balance, amount):
    if amount > 0:
        return balance+amount
    
    print('Ошибка: сумма пополнения должна быть положительной.')
    return balance

def withdraw(balance, amount):
    if amount < 0:
        print('Ошибка: сумма снятия должна быть положительной.')
        return balance
    elif balance - amount < 0:
        print('Ошибка: недостаточно средств на счёте.')
        return balance
    
    return balance - amount 


def main():
    greet_client("Анна","Петрова")

    print(deposit(1000, 500))   # 1500
    print(deposit(1000, -200))  # Ошибка: сумма пополнения должна быть положительной. 1000

    print(withdraw(1000, 300))  # 700
    print(withdraw(1000, 1500)) # Ошибка: недостаточно средств на счёте. 1000
    print(withdraw(1000, -100)) # Ошибка: сумма снятия должна быть положительной. 1000


if __name__ == "__main__":
	main() 
    
