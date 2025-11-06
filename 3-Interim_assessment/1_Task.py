"""
Задача №1. Магическая дата

Это дата, когда день, умноженный на месяц, равен числу, образованному последними двумя цифрами года.

Напишите функцию is_magic(date), которая принимает в качестве аргумента 
строковое представление корректной даты и возвращает:
- True, если дата является магической
- False — в противном случае

Пример использования:
print(is_magic('10.06.1960'))
print(is_magic('11.06.1960'))

Результат (тестовые данные):
Sample Input 1: 10.06.1960
Sample Output 1: True
Sample Input 2: 15.03.1945
Sample Output 2: True

Подсказки к решению
1. Разделение строки по точке
Чтобы получить день, месяц и год отдельно, воспользуйтесь методом .split('.'). 
Он разделит строку по символу точки. 
Метод split() возвращает строки, поэтому нужно преобразовать их в числа.
Для этого используется map(int, ...), который применяет int() ко всем элементам 
списка: day, month, year = map(int, date.split('.'))
2. Получение последних двух цифр года
Используйте оператор % (остаток от деления), чтобы извлечь последние две цифры года
Если произведение дня и месяца равно последним двум цифрам года, то дата — магическая.
3. Программа должна обрабатывать лишние пробелы, на вход могут идти строчки с пробелами (15 . 03.1 94 5)
"""

from datetime import datetime
    

def is_magic(date: str) -> bool:
    try:
        date_parts = list(map(int, date.replace(' ', '', -1).split('.')))
    except ValueError:
        print(f'non-numeric date format: {date}')
        return False

    if len(date_parts) != 3:
        print(f'invalid date format: {date}')
        return False
    
    day, month, year = date_parts
    date_normalized = f'{day}.{month}.{year % 100}' # Нормализуем год

    try:
        datetime.strptime(date_normalized, '%d.%m.%y')
    except ValueError:
        print(f'incorrect date: {date_normalized}')
        return False
    
    return day*month==year


def main():
    print(is_magic('10.06.1960')) # True
    print(is_magic('10.06.60'))   # True
    print(is_magic('15 . 03.1 94 5')) # True

    print(is_magic('11.06.1960')) # False
    print(is_magic('10.VI.1960')) # non-numeric date format: 10.VI.1960  False
    print(is_magic('80.01.80'))   # incorrect date: 80.1.80  False
    print(is_magic('11.01.11'))
    print(is_magic('11.01.1'))


if __name__ == "__main__":
	main() 
