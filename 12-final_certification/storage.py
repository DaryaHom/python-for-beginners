from models import Subscription
from decimal import Decimal
from config import DB_CONFIG
import psycopg2

conn = psycopg2.connect(
    host=DB_CONFIG['host'],
    database=DB_CONFIG['database'], 
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    port=DB_CONFIG['port']
)

cur = conn.cursor()

def save_subscription(s: Subscription):
    """
    Сохраняет новую подписку в БД.
    """
    if not s:
        raise ValueError()
        return
    elif not s.user:
        raise ValueError()
    elif not s.title:
        raise ValueError()
    elif not s.start_date:
        raise ValueError()
    elif not s.end_date:
        raise ValueError()
    elif not s.price:
        raise ValueError()
    
    try:
        cur.execute(
            "INSERT INTO subscriptions \
                (username, title, start_date, end_date, category, price, price_daily, descr) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (s.user, s.title, s.start_date, s.end_date, s.category, s.price, s.price_daily, s.descr)
        )
        conn.commit()
    except Exception as e:  # TODO
        raise e
        

def get_subscriptions() -> list[Subscription]:
    """
    Загружает все операции из БД и возвращает список Subscription.
    """
    subs = []

    try:
        cur.execute(
            "SELECT " \
                "id, " \
                "username, " \
                "title, " \
                "start_date, " \
                "end_date, " \
                "category, " \
                "price, " \
                "price_daily, " \
                "descr " \
            "FROM subscriptions ORDER BY id")
        data = cur.fetchall()
    except Exception as e:  # TODO
        raise e
    try:
        for (id, user, title, start_date, end_date, category, price, price_daily, descr) in data:
            subs.append(
                Subscription(
                    id=id,
                    user=user,
                    title=title,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    category=category,
                    price=price.quantize(Decimal('1.00')),
                    price_daily=price_daily.quantize(Decimal('1.00')),
                    descr=descr,
                )
            )
        return subs
    except Exception as e: # TODO
        raise e

def delete_subscription(id: int):
    try:
        cur.execute("DELETE FROM subscriptions WHERE id = %s", str(id))
        conn.commit()
    except Exception as e:  # TODO
        raise e
