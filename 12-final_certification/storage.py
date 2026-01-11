import psycopg2
from models import Subscription
from config import DB_CONFIG
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import Generator

pool = SimpleConnectionPool(
    minconn=DB_CONFIG['minconn'],
    maxconn=DB_CONFIG['maxconn'],
    host=DB_CONFIG['host'],
    database=DB_CONFIG['database'], 
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    port=DB_CONFIG['port']
)

@contextmanager
def get_connection() -> Generator:
    """
    Контекстный менеджер для получения соединения из пула
    """
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)


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
        start_date=row[3],
        end_date=row[4],
        category=row[5],
        price=row[6],
        price_daily=row[7],
        descr=row[8],
    )


def create_subscription(s: Subscription):
    """
    Создаёт новую подписку в БД

    :param s: Subscription entity
    :type s: Subscription

    :raises RuntimeError: при ошибке БД
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO subscriptions \
                        (username, title, start_date, end_date, category, price, price_daily, descr) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (s.user, s.title, s.start_date, s.end_date, s.category, s.price, s.price_daily, s.descr)
                )
                conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise RuntimeError(f'Не удалось создать подписку: {e}') from e

def get_subscription(id: str) -> Subscription:
    """
    ВОзвращает подписку по её ID.

    :param id: Subscription ID
    :type id: str

    :returns: Subscription entity
    :rtype: Subscription

    :raises RuntimeError: при ошибке БД
    :raises ValueError: если подписка не найдена или некорректна
    :raises TypeError: если подписка не найдена или некорректна
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
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
                    "WHERE id = %s", id)
                data = cur.fetchone()
    except psycopg2.Error as e:
        raise RuntimeError(f'Не удалось получить подписку: {e}') from e   

    if not data:
        raise ValueError('Подписка не найдена')
    
    try:
        sub = _row_to_subscription(data)
    except ValueError as e:
        raise ValueError('Подписка содержит некорректные данные: {e}') from e
    except TypeError as e:
        raise TypeError('Подписка содержит некорректные данные: {e}') from e
    return sub


def get_subscriptions() -> list[Subscription]:
    """
    Возвращает все подписки из БД.

    :returns: Перечень подписок
    :rtype: list[Subscription]

    :raises RuntimeError: при ошибке БД
    :raises ValueError: если подписки содержат некорректные данные
    :raises TypeError: если подписки содержат некорректные данные
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
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
    except psycopg2.Error as e:
        raise RuntimeError(f'Не удалось получить подписки: {e}') from e   

    try:
        res = [_row_to_subscription(row) for row in data]
    except ValueError as e:
        raise ValueError('Подписки содержат некорректные данные: {e}') from e
    except TypeError as e:
        raise TypeError('Подписки содержат некорректные данные: {e}') from e
    return res

    
def update_subscription(s: Subscription):
    """
    Обновляет существующую подписку.

    :param s: Subscription entity
    :type s: Subscription

    :raises RuntimeError: при ошибке БД
    """
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
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
    except psycopg2.Error as e:
        conn.rollback()
        raise RuntimeError(f'Не удалось обновить подписку: {e}') from e 
        

def delete_subscription(id: str):
    """
    Удаляет подписку по ID.

    :param id: Subscription ID
    :type id: str
    :raises RuntimeError: при ошибке БД
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM subscriptions WHERE id = %s", id)
                conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise RuntimeError(f'Не удалось удалить подписку: {e}') from e 
    