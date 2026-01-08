from datetime import datetime
from decimal import Decimal

import enum

@enum.unique
class Category(enum.Enum):
    """
    Категории подписочных сервисов.
    """
    MUSIC = "Музыка"
    VIDEO = "Видео и стриминг"
    PODCASTS = "Подкасты"
    GAMING = "Игры"
    CLOUD_STORAGE = "Облачное хранилище" 
    HOSTING = "Хостинг и домены"
    SOFTWARE = "Программное обеспечение"
    EDUCATION = "Образование"
    NEWS = "СМИ"
    FITNESS = "Фитнес и здоровье"
    BEAUTY = "Косметика и салоны красоты"
    SHOPPING = "Шоппинг и доставка"
    TRANSPORT = "Транспорт и такси" 
    CHARITY = "Благотворительность"  
    FINANCE = "Финансы и инвестиции"   
    TELECOM = "Телеком, связь и общение"   
    PRODUCTIVITY = "Продуктивность"
    TRAVEL = "Путешествия"
    FOOD = "Еда и доставка"
    PET_CARE = "Уход за животными" 
    OTHER = "Это другоэ"

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
            start_date: str, 
            end_date: str, 
            category: str, 
            id: str | None = None,
            price: Decimal | None = None, 
            price_daily: Decimal | None = None, 
            descr = '',
        ):

        if not isinstance(user, str):
            raise TypeError("Имя пользователя должно быть строкой")
        if not user.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        
        if not isinstance(title, str):
            raise TypeError("Название подписки должно быть строкой")
        if not title.strip():
            raise ValueError("Название подписки не может быть пустым")
        
        if not isinstance(start_date, str):
            raise TypeError("Дата начала подписки должна быть строкой")
        if not start_date.strip():
            raise ValueError("Дата начала подписки не может быть пустой")
        
        if not isinstance(end_date, str):
            raise TypeError("Дата истечения подписки должна быть строкой")
        if not end_date.strip():
            raise ValueError("Дата истечения подписки не может быть пустой")
        
        if not isinstance(category, str):
            raise TypeError("Категория подписки должна быть строкой")
        if not category.strip():
            raise ValueError("Категория подписки не может быть пустой")
        
        if not Category.has_value(category): 
            raise ValueError("Категория подписки должна быть из указанного списка")
        
        if not isinstance(price, Decimal | None):
            raise TypeError("Цена подписки должна быть строкой")
        
        if not isinstance(price_daily, Decimal | None):
            raise TypeError("Ежедневная оплата подписки должна быть числом")
        
        if not price and not price_daily:
            raise ValueError("Цена подписки не может быть пустой")
        
        if not isinstance(descr, str):
            raise TypeError("Описание должно быть строкой")
        
        if id:
            if not id.isdigit():
                raise ValueError("id должен быть представлен цифрами")
        
        self.id = id        
        self.user = user
        self.title = title
        try: 
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except:
            pass # TODO

        if not price:
            self.price = (self.end_date-self.start_date).days * price_daily
        else:
            self.price = price

        if not price_daily:
            days_diff = (self.end_date - self.start_date).days
            if days_diff > 0:
                self.price_daily = price / days_diff
            else:
                self.price_daily = price
        else:
            self.price_daily = price_daily
        
        self.category = category
        self.descr = descr
