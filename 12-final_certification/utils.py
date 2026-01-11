from datetime import datetime
from decimal import Decimal
from forms import SubscriptionForm
from models import (
    Subscription, 
    PriceCalculator
)


def build_subscription(form: SubscriptionForm, id: str | None = None) -> Subscription:
    """
    Формирует Subscription (entity) из провалидированной формы.

    :param form: Валидная форма подписки
    :type form: SubscriptionForm
    :param id: Идентификатор подписки
    :type id: str | None

    :returns: Subscription
    :rtype: Subscription

    :raise: 
    """

    start_date, end_date = None, None
    try: 
        start_date = datetime.strptime(form.start_date.data.strip(), '%Y-%m-%d')
    except:
        raise ValueError('Дата начала подписки должна быть в формате YYYY-MM-DD')
    try: 
        end_date = datetime.strptime(form.end_date.data.strip(), '%Y-%m-%d')
    except:
        raise ValueError('Дата окончания подписки должна быть в формате YYYY-MM-DD')
    
    price, price_daily = 0,0
    try:
        price, price_daily = PriceCalculator.calculate_price(
            start_date, 
            end_date, 
            form.price.data,
            form.price_daily.data,
        )
    except ValueError as e:
        raise ValueError(f'Ошибка расчёта цены: {e}') from e   
    except TypeError as e:
        raise TypeError(f'Ошибка расчёта цены: {e}') from e   

    return Subscription(
        id=id,
        user=form.user.data,
        title=form.title.data,
        category=form.category.data,
        start_date=start_date,
        end_date=end_date,
        price=price,
        price_daily=price_daily,
        descr=form.descr.data,
    )
