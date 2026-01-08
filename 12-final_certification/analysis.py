import pandas as pd
import matplotlib.pyplot as plt
from storage import get_subscriptions

def subscriptions_to_df() -> pd.DataFrame:
    """
    Загружает подписки из хранилища и преобразует их в pandas.DataFrame
    """
    subs = get_subscriptions()
    rows = []

    for s in subs:
        rows.append({
            "id": s.id,
            "user": s.user,
            "title": s.title,
            "category": s.category,
            "start_date": pd.to_datetime(s.start_date),
            "end_date": pd.to_datetime(s.end_date),
            "price": float(s.price) if s.price else None,
            "price_daily": float(s.price_daily) if s.price_daily else None,
        })

    return pd.DataFrame(rows)

def expenses_for_period(start: str, end: str) -> pd.DataFrame:
    """
    Рассчитывает расходы по подпискам за указанный период
    """
    df = subscriptions_to_df()

    if df.empty:
        return df

    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    df = df[(df["start_date"] <= end_dt) & (df["end_date"] >= start_dt)]

    def calc_cost(row):
        period_start = max(row["start_date"], start_dt)
        period_end = min(row["end_date"], end_dt)
        days = (period_end - period_start).days + 1

        if row["price_daily"] is not None:
            return days * row["price_daily"]

        return row["price"] or 0

    df["cost"] = df.apply(calc_cost, axis=1)
    return df


def expenses_by_category(start: str, end: str) -> pd.Series:
    """
    Агрегация расходов по категориям
    """
    df = expenses_for_period(start, end)

    if df.empty:
        return pd.Series(dtype=float)

    return (
        df.groupby("category")["cost"]
        .sum()
        .sort_values(ascending=False)
    )


def total_expenses(start: str, end: str) -> float:
    """
    Общая сумма расходов за период
    """
    df = expenses_for_period(start, end)
    return float(df["cost"].sum()) if not df.empty else 0.0


def plot_category_pie(start: str, end: str):
    """
    Круговая диаграмма расходов по категориям
    """
    data = expenses_by_category(start, end)

    if data.empty:
        print("Нет данных для визуализации")
        return

    plt.figure(figsize=(6, 6))
    data.plot.pie(autopct="%1.1f%%")
    plt.title("Структура расходов по категориям")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def plot_expenses_over_time(start: str, end: str):
    """
    Динамика расходов по месяцам
    """
    df = expenses_for_period(start, end)

    if df.empty:
        print("Нет данных для визуализации")
        return

    df["month"] = df["start_date"].dt.to_period("M")
    grouped = df.groupby("month")["cost"].sum()

    plt.figure(figsize=(8, 4))
    grouped.plot(kind="bar")
    plt.title("Расходы по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Сумма")
    plt.tight_layout()
    plt.show()
