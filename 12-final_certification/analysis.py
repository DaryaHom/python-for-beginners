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
            'id': s.id,
            'user': s.user,
            'title': s.title,
            'category': s.category,
            'start_date': pd.to_datetime(s.start_date),
            'end_date': pd.to_datetime(s.end_date),
            'price': float(s.price) if s.price else None,
            'price_daily': float(s.price_daily) if s.price_daily else None,
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

    # Переопределяем датафрейм, так, чтобы он включал только те подписки,
    # которые относятся к указанному периоду времени
    df = df[(df['start_date'] <= end_dt) & (df['end_date'] >= start_dt)]

    def calc_cost(row):
        period_start = max(row['start_date'], start_dt)
        period_end = min(row['end_date'], end_dt)
        days = (period_end - period_start).days + 1
        if row['start_date'] >= period_start and row['end_date'] <= period_end:
            return row['price']
        return days * row['price_daily']

    df['cost'] = df.apply(calc_cost, axis=1)
    return df


def expenses_by_category(start: str, end: str) -> pd.Series:
    """
    Агрегация расходов по категориям
    """
    df = expenses_for_period(start, end)

    if df.empty:
        return pd.Series(dtype=float)

    return (
        df.groupby('category')['cost']
        .sum()
        .sort_values(ascending=False)
    )


def total_expenses(start: str, end: str) -> float:
    """
    Общая сумма расходов за период
    """
    df = expenses_for_period(start, end)
    return float(df['cost'].sum()) if not df.empty else 0.0


def plot_category_pie(start: str, end: str):
    """
    Круговая диаграмма расходов по категориям
    """
    data = expenses_by_category(start, end)

    if data.empty:
        print('Нет данных для визуализации')
        return

    plt.figure(figsize=(6, 6))
    data.plot.pie(autopct='%1.1f%%')
    plt.title('Структура расходов по категориям')
    plt.tight_layout()
    plt.show()
