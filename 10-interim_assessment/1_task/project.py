"""
3. Класс Project
Атрибуты:
	title — название проекта
	tasks — список задач (объекты Task)

Методы:
	add_task(task) — добавляет задачу к проекту
	project_progress() — возвращает процент завершения проекта на основе статуса задач
"""
from task import Task, STATUS_COMPLETE

class Project:
    def __init__(self,
            title: str,
            tasks: list[Task] = None,
        ):
        if not isinstance(title, str):
            raise TypeError("Название проекта должно быть строкой")
        if not title.strip():
            raise ValueError("Название проекта не может быть пустым")  
        
        if not isinstance(tasks, list | None):
            raise TypeError("Неверный тип списка задач")
        
        self._title = title
        if tasks is None:
            self._tasks = []
        else:
            self._tasks = tasks    

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def tasks(self) -> list[Task]:
        return self._tasks.copy()
        
    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("Неверный тип задачи")
        
        self._tasks.append(task)
        
    def project_progress(self) -> float:
        count = len(self._tasks)
        if not count:
            return 0
        
        total_percent = 0
        for i in self._tasks:
            if i.status == STATUS_COMPLETE:
                total_percent +=100
        
        return round(total_percent / count, 2)
