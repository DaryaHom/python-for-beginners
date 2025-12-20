"""
Задание №2.
Создайте класс Product, который содержит информацию о товаре: название, цена, количество на складе. 
Реализуйте методы для изменения количества и получения общей стоимости товаров.
Добавьте метод для применения скидки к товару 
"""

from decimal import *

class Product:
    def __init__(self, name: str, price: Decimal, count: int):
        if not isinstance(name, str):
            raise TypeError("Название товара должно быть строкой")
        if not name.strip():
            raise ValueError("Название товара не может быть пустым")
        
        if not isinstance(price, Decimal):
            raise TypeError("Цена должна быть числом")
        if price <= 0:
            raise ValueError("Цена не может быть отрицательной или отсутствовать")
        
        if not isinstance(count, int):
            raise TypeError("Количество должно быть целым числом")
        if count < 0:
            raise ValueError("Количество не может быть отрицательным")

        self._name = name
        self._price = price
        self._count = count

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Количество должно быть целым числом")
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._count = value

    def total_cost(self) -> Decimal:
        return self.price*self.count
    
    # Скидка в процентах, с округлением до целого
    def get_discounted_price(self, discount_percent: int) -> Decimal:
        if 0 >= discount_percent >= 100:
            raise ValueError("Скидка должна быть в диапазоне от 0 до 100%")
        return self.price - (self.price * discount_percent/100)


p = Product("book", Decimal('30'), 2)
p.count = 4
print('Количество товара: ', p.count)
print('Общая стоимость: ', p.total_cost())
print('Цена со скидкой 10%: ', p.get_discounted_price(10))

