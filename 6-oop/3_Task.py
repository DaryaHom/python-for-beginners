"""
Задание №3**. 
1. Создайте класс Animal.
В конструкторе __init__ он должен принимать:
        - name
        - age

Добавьте два метода:
	1. eat() — выводит сообщение вида: "{self.name} ест."
	2. make_sound() — выводит универсальное сообщение вида: "{self.name} издает звук."

2. Создайте класс Dog, который наследуется от Animal.
В конструкторе __init__ должен принимать:
       - name
       - age
       - breed (порода)
Используйте super() для вызова конструктора родителя.
Переопределите метод make_sound() так, чтобы он выводил "Гав!".
Добавьте уникальный метод fetch(), который выводит "{self.name} принес(ла) палку."

3. Класс-наследник Cat
Создайте класс Cat, который наследуется от Animal.
Конструктор должен принимать:
	- name
	- age

Используйте super().
Переопределите метод make_sound(), чтобы он выводил "Мяу!".
Добавьте уникальный метод purr(), который выводит "{self.name} мурлычет."

4. Многоуровневое наследование — Parrot
Создайте класс Bird, который наследуется от Animal.
Добавьте уникальный метод fly(), который выводит "{self.name} летит."
Создайте класс Parrot, который наследуется от Bird.
Переопределите метод make_sound(), чтобы он выводил "Кар! Я хороший!"

5. Собираем всех в зоопарке
Создайте по одному объекту каждого класса:
	- Dog
	- Cat
	- Parrot

Поместите все объекты в список zoo_animals.
Напишите цикл:
- Для каждого животного в списке вызывайте метод make_sound().
Каждое животное издает свой уникальный звук, несмотря на одинаковый метод.
"""


class Animal:
    def __init__(self, name: str, age: float | int):
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой")
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        
        if not isinstance(age, (float,int)):
            raise TypeError("Возраст должен быть числом")
        if age < 0:
            raise ValueError("Возраст должен быть положительным")
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        return self._name
    
    def eat(self):
        print(f'{self.name} ест.')

    def make_sound(self):
        print(f'{self.name} издает звук.')

class Dog(Animal):
    def __init__(self, name: str, age: float | int, breed: str):
        super().__init__(name, age)

        if not isinstance(breed, str) or not breed.strip():
            raise ValueError("Порода должна быть непустой строкой")
        self._breed = breed

    def make_sound(self):
        print('Гав!')

    def fetch(self):
        print(f'{self.name} принес(ла) палку.')


class Cat(Animal):
    def make_sound(self):
        print('Мяу!')

    def purr(self):
        print(f'{self.name} мурлычет.')

class Bird(Animal):
    def fly(self):
        print(f'{self.name} летит.')

class Parrot(Bird):
    def make_sound(self):
        print('Кар! Я хороший!')

zoo_animals = [
    Dog('Sharik', 1.0, 'Dvor-terier'), 
    Cat('Murzik', 2), 
    Parrot('Popka', 3)]

for animal in zoo_animals:
    animal.make_sound()
