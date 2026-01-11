from datetime import datetime
from decimal import Decimal

import enum

class PriceCalculator:
    @staticmethod
    def calculate_price(
            start_date: datetime, 
            end_date: datetime, 
            price: Decimal|None = None, 
            price_daily: Decimal|None =None
        ) -> tuple[Decimal, Decimal]: 
        """
        Вычисляет цену и дневную ставку на основе начальной и конечной даты

        :param start_date: Дата начала периода
        :type start_date: datetime
        :param end_date: Дата окончания периода
        :type end_date: datetime
        :param price: Общая цена за весь период. Если не указана, вычисляется из `price_daily`
        :type price: Decimal or None
        :param price_daily: Цена за один день. Используется, если не указана общая цена
        :type price_daily: Decimal or None

        :return: Кортеж из общей цены и дневной ставки.
        :rtype: tuple[Decimal, Decimal]

        :raises ValueError: Если не указаны ни `price`, ни `price_daily`.
        :raises TypeError: Если `start_date` или `end_date` не являются `datetime`
        :raises TypeError: Если `price` или `price_daily` не являются `Decimal`
        """
        if not isinstance(start_date, datetime):
            raise TypeError('start_date должен быть типа datetime')
        if not isinstance(end_date, datetime):
            raise TypeError('end_date должен быть типа datetime')
        if not isinstance(price, Decimal|None):
            raise TypeError('price должен быть типа Decimal')
        if not isinstance(price_daily, Decimal|None):
            raise TypeError('price_daily должен быть типа Decimal')

        if not price and not price_daily:
            raise ValueError('Цена не установлена') 
        
        if not price:
            price = (end_date-start_date).days * price_daily
        else:
            price = price

        if not price_daily:
            days_diff = (end_date - start_date).days
            if days_diff > 0:
                price_daily = price / days_diff
            else:
                price_daily = price

        return price, price_daily
    

@enum.unique
class Category(enum.Enum):
    """
    Категории подписочных сервисов.
    """
    MUSIC = 'Музыка'
    VIDEO = 'Видео и стриминг'
    PODCASTS = 'Подкасты'
    GAMING = 'Игры'
    CLOUD_STORAGE = 'Облачное хранилище' 
    HOSTING = 'Хостинг и домены'
    SOFTWARE = 'Программное обеспечение'
    EDUCATION = 'Образование'
    NEWS = 'СМИ'
    FITNESS = 'Фитнес и здоровье'
    BEAUTY = 'Косметика и салоны красоты'
    SHOPPING = 'Шоппинг и доставка'
    TRANSPORT = 'Транспорт и такси' 
    CHARITY = 'Благотворительность'  
    FINANCE = 'Финансы и инвестиции'   
    TELECOM = 'Телеком, связь и общение'   
    PRODUCTIVITY = 'Продуктивность'
    TRAVEL = 'Путешествия'
    FOOD = 'Еда и доставка'
    PET_CARE = 'Уход за животными' 
    OTHER = 'Это другоэ'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 
    
    @classmethod
    def choices(cls):
        return [(item.value, item.value) for item in cls]
    
class Subscription:
    def __init__(
            self, 
            # личное приложение, не имеет смысла создавать отдельный класс пользователя
            user: str,
            title: str, 
            category: str, 
            start_date: datetime, 
            end_date: datetime, 
            price: Decimal, 
            price_daily: Decimal ,
            id: str | None = None, 
            descr: str = '',
        ):
        if id and not id.isdigit():
            raise ValueError('id должен быть представлен цифрами')
            
        if not isinstance(user, str):
            raise TypeError('Имя пользователя должно быть строкой')
        if not user.strip():
            raise ValueError('Имя пользователя не может быть пустым')
        
        if not isinstance(title, str):
            raise TypeError('Название подписки должно быть строкой')
        if not title.strip():
            raise ValueError('Название подписки не может быть пустым')
        
        if not isinstance(category, str):
            raise TypeError('Категория подписки должна быть строкой')
        if not category.strip():
            raise ValueError('Категория подписки не может быть пустой')
        
        if not Category.has_value(category): 
            raise ValueError('Категория подписки должна быть из указанного списка')
        
        if not isinstance(start_date, datetime):
            raise TypeError('Дата начала подписки должна быть datetime')
        
        if not isinstance(end_date, datetime):
            raise TypeError('Дата истечения подписки должна быть datetime')
        
        days_diff = (end_date - start_date).days
                
        if days_diff < 0:
            raise ValueError('Дата начала подписки не может быть позже даты окончания')
        
        if not isinstance(price, Decimal):
            raise TypeError('Цена подписки должна быть числом')
        
        if not isinstance(price_daily, Decimal):
            raise TypeError('Ежедневная оплата подписки должна быть числом')
        
        if price < 0 or price_daily < 0:
            raise ValueError('Цена подписки не может быть отрицательной')
                
        if abs(price - price_daily * days_diff) > 0.01:  # допуск 0.01 рубля
            raise ValueError('Ежедневная цена не совпадает с итоговой')
        
        if not isinstance(descr, str):
            raise TypeError('Описание должно быть строкой')
        
        self.id = id        
        self.user = user
        self.title = title
        self.category = category
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.price_daily = price_daily
        self.descr = descr
