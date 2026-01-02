"""
2. Класс Task
Атрибуты:
	title — название задачи
	description — описание задачи
	status — статус задачи ("В процессе", "Завершено")
	assigned_employee — назначенный сотрудник (объект класса Employee)

Методы:
	assign_employee(employee) — назначает задачу сотруднику
	mark_complete() — отмечает задачу как завершённую
"""

from employee import Employee

STATUS_CREATED = 'Created'
STATUS_PROGRESS = 'Progress'
STATUS_COMPLETE = 'Complete'

class Task:
    def __init__(self,
        title: str,
        description: str='',
        status: str=STATUS_CREATED,
        assigned_employee: Employee=None,
    ):
        if not isinstance(title, str):
            raise TypeError("Название задачи должно быть строкой")
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")    
        
        if not isinstance(description, str):
            raise TypeError("Описание задачи должно быть строкой")
        
        if not isinstance(status, str):
            raise TypeError("Статус задачи должен быть строкой")
        if status != STATUS_CREATED and status != STATUS_PROGRESS and status != STATUS_COMPLETE:
            raise ValueError("Некорректный статус задачи")
        
        if not isinstance(assigned_employee, Employee | None):
            raise TypeError("Должен быть указан исполнитель задачи")
        
        self._title = title
        self._description = description
        self._status = status
        self._assigned_employee = assigned_employee

    @property
    def status(self) -> str:
        return self._status

    @property
    def assigned_employee(self) -> Employee | None:
        return self._assigned_employee
    
    def assign_employee(self, employee: Employee):
        if not isinstance(employee, Employee):
            raise TypeError("Должен быть указан исполнитель задачи")
        if employee is None:
            raise ValueError("Исполнитель задачи не может быть пустым")  
        self._assigned_employee = employee

    def mark_complete(self):
        self._status = STATUS_COMPLETE
