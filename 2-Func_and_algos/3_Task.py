"""
### Задача №3 (ДОПОЛНИТЕЛЬНАЯ). Программа для мини-банка (версия со словарём)

Дан словарь `clients`, где ключи — полные имена клиентов (`"Имя Фамилия"`), а значения — их балансы (целые числа).  
Реализуйте три функции, которые принимают этот словарь и изменяют его напрямую:

1. `greet_client(clients, first_name, last_name)`  
   — выводит приветствие в зависимости от текущего времени суток в Москве:  
   - 6:00–11:59 → «Доброе утро»  
   - 12:00–17:59 → «Добрый день»  
   - 18:00–23:59 → «Добрый вечер»  
   - 0:00–5:59 → «Доброй ночи»  
   Если клиента нет в словаре — выводит ошибку.

2. `deposit(clients, first_name, last_name, amount)`  
   — увеличивает баланс клиента на `amount`, если:  
   - клиент существует,  
   - `amount > 0`.  
   При ошибке — выводит сообщение. Успешное пополнение подтверждается сообщением с новым балансом.

3. `withdraw(clients, first_name, last_name, amount)`  
   — уменьшает баланс на `amount`, если:  
   - клиент существует,  
   - `amount > 0`,  
   - средств достаточно.  
   Иначе — выводит соответствующую ошибку.

Данные меняются напрямую в словаре, операции изменяют исходный словарь напрямую.

### Примеры использования

```python
# Создаём словарь клиентов
clients = {
    "Анна Петрова": 1000,
    "Иван Сидоров": 500
}

# Приветствие
greet_client(clients, "Анна", "Петрова")
# Вывод (время берется так же по Москве): Добрый день, Анна Петрова!
# Пример для 14:00 для Анны

# Пополнение
deposit(clients, "Анна", "Петрова", 200)
# Вывод: Счёт Анна Петрова пополнен. Новый баланс: 1200

# Снятие
withdraw(clients, "Иван", "Сидоров", 300)
# Вывод: Со счёта Иван Сидоров снято 300. Новый баланс: 200

# Ошибки
deposit(clients, "Мария Иванова", 100)      # Ошибка: клиент не найден
withdraw(clients, "Анна", "Петрова", -50)   # Ошибка: сумма должна быть положительной
withdraw(clients, "Иван", "Сидоров", 1000)  # Ошибка: недостаточно средств

# Проверка итогового состояния
print(clients)
# {'Анна Петрова': 1200, 'Иван Сидоров': 200}
"""

from datetime import datetime, time 
import pytz                           # pip install pytz==2025.2

_MORNING_START = time.fromisoformat('06:00')
_MORNING_END = time.fromisoformat('11:59')

_DAY_START = time.fromisoformat('12:00')
_DAY_END = time.fromisoformat('17:59')

_EVENING_START = time.fromisoformat('18:00')
_EVENING_END = time.fromisoformat('23:59')

_MOSCOW_TIMEZONE = 'Europe/Moscow'

clients = {
    "Анна Петрова": 1000,
    "Иван Сидоров": 500
}

def get_full_name(first_name: str, last_name: str) -> str:
    return f'{first_name} {last_name}'

def search_client(clients: dict[str, int], client_name: str) -> bool:
    if clients[client_name]:
        return True
    
    return False

def get_greeting() -> str:
    moscow_time = datetime.now(pytz.timezone(_MOSCOW_TIMEZONE)).time()

    greeting = 'Доброй ночи'
    if _MORNING_START <= moscow_time <= _MORNING_END:
        greeting = 'Доброе утро' 
    elif _DAY_START <= moscow_time <= _DAY_END:
        greeting = 'Добрый день'
    elif _EVENING_START <= moscow_time <= _EVENING_END:
        greeting = 'Добрый вечер'

    return greeting


def greet_client(clients, first_name, last_name):
    full_name = get_full_name(first_name, last_name)
    
    if not search_client(clients, full_name):
        return
    
    greeting = get_greeting()
    
    print(f'{greeting}, {full_name}!')
    
def deposit(clients, first_name, last_name, amount):
    full_name = get_full_name(first_name, last_name)

    if not search_client(clients, full_name):
        return
    
    if amount < 0:
        print('Ошибка: сумма пополнения должна быть положительной.')
        return 
    
    clients[full_name] = clients[full_name]+amount
    print(f'Счёт {full_name} пополнен. Новый баланс: {clients[full_name]}')


def withdraw(clients, first_name, last_name, amount):
    full_name = get_full_name(first_name, last_name)

    if not search_client(clients, full_name):
        return
    
    if amount < 0:
        print('Ошибка: сумма должна быть положительной')
        return 
    
    curr_balance = clients[full_name]
    if curr_balance - amount < 0:
        print('Ошибка: недостаточно средств')
        return
    
    clients[full_name] = curr_balance - amount 
    print(f'Со счёта {full_name} снято {amount}. Новый баланс: {clients[full_name]}')


def main():
    greet_client(clients, "Анна","Петрова")

    deposit(clients, "Анна", "Петрова", 200)   # Счёт Анна Петрова пополнен. Новый баланс: 1200
    withdraw(clients, "Иван", "Сидоров", 300)  # Со счёта Иван Сидоров снято 300. Новый баланс: 200
    
    # deposit(clients, "Мария Иванова", 100)     # Ошибка: клиент не найден

    withdraw(clients, "Анна", "Петрова", -50)  # Ошибка: сумма должна быть положительной
    withdraw(clients, "Иван", "Сидоров", 1000) # Ошибка: недостаточно средств


if __name__ == "__main__":
	main() 
    
