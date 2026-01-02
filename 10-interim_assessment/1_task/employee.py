"""
Задание №1.
Создайте приложение для учета рабочего времени и задач сотрудников в компании.
Не забывайте про принципы ООП, их можно и нужно применять
(к примеру, сокрытие внутренней реализации - инкапсулирование, уровни доступа к данным).

1. Класс Employee
Атрибуты:
	name — имя сотрудника
	position — должность
	salary — зарплата
	hours_worked — отработанное время в часах (по умолчанию 0)

Методы:
	add_hours(hours) — добавляет отработанные часы
	calculate_pay() — возвращает зарплату на основе отработанных часов, 
    считая ставку как месячную зарплату, делённую на 160 часов
"""
from decimal import Decimal

_HOURS_IN_MONTH = 160

class Employee:
    def __init__(self, 
        name: str, 
        position: str, 
        salary: Decimal, 
        hours_worked: int=0,
    ):
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой")
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        
        if not isinstance(position, str):
            raise TypeError("Должность должна быть строкой")
        if not position.strip():
            raise ValueError("Должность не может отсутствовать")
        
        if not isinstance(salary, Decimal):
            raise TypeError("Заработная плата должна быть числом")
        if salary <= 0:
            raise ValueError("Заработная плата должна быть больше 0")
        
        if not isinstance(hours_worked, int):
            raise TypeError("Отработанные часы должны быть числом")
        if hours_worked < 0:
            raise ValueError("Отработанные часы не могут быть отрицательными")
        
        self._name = name
        self._position = position
        self._salary = salary
        self._hours_worked = hours_worked


    @property
    def name(self) -> str:
        return self._name
    
    @property
    def hours_worked(self) -> int:
        return self._hours_worked
    
    def add_hours(self, hours: int):
        if not isinstance(hours, int):
            raise TypeError("Отработанные часы должны быть числом")
        if hours < 0:
            raise ValueError("Отработанные часы не могут быть отрицательными")
        
        self._hours_worked += hours

    def calculate_pay(self) -> Decimal:
        return (self._hours_worked * (self._salary/_HOURS_IN_MONTH)).quantize(Decimal('1.00'))
