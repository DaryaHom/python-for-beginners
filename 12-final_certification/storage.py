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


def _row_to_subscription(row: dict) -> Subscription:
    """
    Преобразует row базы данных в объект Subscription.

    :param row: Database row
    :type row: dict

    :returns: Subscription entity
    :rtype: Subscription
    """
    return Subscription(
        id=str(row[0]),
        user=row[1],
        title=row[2],
        start_date=row[3].strftime('%Y-%m-%d'),
        end_date=row[4].strftime('%Y-%m-%d'),
        category=row[5],
        price=row[6].quantize(Decimal('1.00')),
        price_daily=row[7].quantize(Decimal('1.00')),
        descr=row[8],
    )


def create_subscription(s: Subscription):
    """
    Создаёт новую подписку в БД

    :param s: Subscription entity
    :type s: Subscription
    """
    cur.execute(
        "INSERT INTO subscriptions \
            (username, title, start_date, end_date, category, price, price_daily, descr) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (s.user, s.title, s.start_date, s.end_date, s.category, s.price, s.price_daily, s.descr)
    )
    conn.commit()


def get_subscription(id: str) -> Subscription:
    """
    ВОзвращает подписку по её ID.

    :param id: Subscription ID
    :type id: str

    :returns: Subscription entity
    :rtype: Subscription

    :raises ValueError: если подписка не найдена
    """

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
        "FROM subscriptions " \
        "WHERE id = {0}".format(id))
    data = cur.fetchone()

    if not data:
        raise ValueError("Subscription not found")
   
    return _row_to_subscription(data)


def get_subscriptions() -> list[Subscription]:
    """
    Возвращает все подписки из БД.

    :returns: Перечень подписок
    :rtype: list[Subscription]
    """

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

    return [_row_to_subscription(row) for row in data]

    
def update_subscription(s: Subscription):
    """
    Обновляет существующую подписку.

    :param s: Subscription entity
    :type s: Subscription
    """
    
    cur.execute(
        "UPDATE subscriptions \
        SET " \
            "username = %s, " \
            "title = %s, " \
            "start_date = %s, " \
            "end_date = %s, " \
            "category = %s, " \
            "price = %s, " \
            "price_daily = %s, " \
            "descr = %s \
        WHERE id = %s",
        (s.user, s.title, s.start_date, s.end_date, s.category, s.price, s.price_daily, s.descr, s.id)
    )
    conn.commit()
        

def delete_subscription(id: str):
    """
    Удаляет подписку по ID.

    :param id: Subscription ID
    :type id: str
    """
    cur.execute("DELETE FROM subscriptions WHERE id = {0}".format(id))
    conn.commit()
    