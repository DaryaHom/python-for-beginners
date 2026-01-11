"""
Модуль аналитики подписок.

Предназначен для анализа данных о подписках пользователя.
Использует pandas для обработки данных и matplotlib для визуализации.

Основные возможности:
- преобразование подписок из хранилища в pandas.DataFrame;
- расчёт расходов за произвольный период времени;
- агрегация расходов по категориям;
- подсчёт общей суммы расходов;
- построение круговой диаграммы структуры расходов.

Модуль используется в web-приложении (Flask) на странице аналитики.

Все даты передаются и обрабатываются в формате `YYYY-MM-DD`

:depends:
    - pandas
    - matplotlib
    - storage.get_subscriptions
"""
import io, base64, logging
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from storage import get_subscriptions

class AnalyticsError(Exception):
    """
    Исключение, возникающее при ошибках в модуле аналитики.
    """
    pass


def subscriptions_to_df() -> pd.DataFrame:
    """
    Преобразует подписки из хранилища в pandas.DataFrame.

    Загружает все подписки с помощью `storage.get_subscriptions` и
    формирует DataFrame для дальнейшего анализа.

    :returns: DataFrame со всеми подписками
    :rtype: pandas.DataFrame

    :raises AnalyticsError: Не удалось загрузить данные о подписках или данные некорректны
    """

    try:
        subs = get_subscriptions()
    except (TypeError, ValueError, RuntimeError) as e:
        raise AnalyticsError('Не удалось загрузить данные о подписках') from e
    
    rows = []
    try: 
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
    except (ValueError, TypeError) as e:
        raise AnalyticsError(f'Некорректная подписка, id={s.id}') from e

    return pd.DataFrame(rows)

def expenses_for_period(start: str, end: str) -> pd.DataFrame:
    """
    Рассчитывает расходы по подпискам за указанный период времени.

    Для каждой подписки определяется пересечение с заданным периодом.
    Если подписка полностью попадает в период - используется полная цена.
    Если подписка покрывает период частично - стоимость рассчитывается
    исходя из ежедневной цены.

    :param start: дата начала периода
    :type start: str
    :param end: дата окончания периода
    :type end: str

    :returns: DataFrame с добавленным столбцом `cost`
    :rtype: pandas.DataFrame

    :raises AnalyticsError: Если не удалось преобразовать подписки в df
    :raises AnalyticsError: Если не удалось преобразовать время в datetime
    """
    try:
        df = subscriptions_to_df()
    except AnalyticsError as e:
        raise e 

    if df.empty:
        return df

    try:
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
    except (ValueError, TypeError) as e:
        raise AnalyticsError("Неверный формат даты. Ожидается YYYY-MM-DD.") from e

    # Переопределяем датафрейм, так, чтобы он включал только те подписки,
    # которые относятся к указанному периоду времени
    df = df[(df['start_date'] <= end_dt) & (df['end_date'] >= start_dt)]

    def calc_cost(row):
        period_start = max(row['start_date'], start_dt)
        period_end = min(row['end_date'], end_dt)
        days = (period_end - period_start).days + 1
        # Если подписка входит в указанный период целиком, то возвращаем fullprice
        if row['start_date'] >= period_start and row['end_date'] <= period_end:
            return row['price']
        return days * row['price_daily']

    df['cost'] = df.apply(calc_cost, axis=1)
    return df


def expenses_by_category(start: str, end: str) -> pd.Series:
    """
    Выполняет агрегацию расходов по категориям.

    Использует данные, рассчитанные функцией
    `expenses_for_period`, и суммирует расходы
    по каждой категории.

    :param start: дата начала периода
    :type start: str
    :param end: дата окончания периода
    :type end: str

    :returns: Перечень расходов по категориям
    :rtype: pandas.Series

    :raises AnalyticsError: Если не удалось расчитать стоимость за период
    """
    try:
        df = expenses_for_period(start, end)
    except AnalyticsError as e:
        raise e 

    if df.empty:
        return pd.Series(dtype=float)

    return (
        df.groupby('category')['cost']
        .sum()
        .sort_values(ascending=False)
    )


def total_expenses(start: str, end: str) -> float:
    """
    Рассчитывает общую сумму расходов за период.

    :param start: дата начала периода
    :type start: str
    :param end: дата окончания периода
    :type end: str

    :returns: общая сумма расходов
    :rtype: float

    :raises AnalyticsError: Если не удалось расчитать стоимость за период
    """
    try:
        df = expenses_for_period(start, end)
    except AnalyticsError as e:
        raise e 
    
    return float(df['cost'].sum()) if not df.empty else 0.0


def plot_category_pie(start: str, end: str) -> str:
    """
    Строит круговую диаграмму расходов по категориям.

    Диаграмма отражает процентное распределение
    расходов за выбранный период времени.

    :param start: дата начала периода
    :type start: str
    :param end: дата окончания периода
    :type end: str

    :returns: Диаграмма в base64
    :rtype: str
    :raises AnalyticsError: Если не удалось построить график
    """
    data = expenses_by_category(start, end)

    if data.empty:
        logging.info('Нет данных для визуализации')
        return ''

    try:
        plt.figure(figsize=(6, 6))
        data.plot.pie(autopct='%1.1f%%')
        plt.title('Структура расходов по категориям')
        plt.tight_layout()
        plt.ylabel("")

         # Сохраняем в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()  # Важно закрыть фигуру
        buf.seek(0)
         # Кодируем в base64 для HTML
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        raise AnalyticsError('Не удалось построить график') from e

