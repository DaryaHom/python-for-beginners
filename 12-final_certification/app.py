"""
Транспортный уровень приложения. 

Модуль содержит роуты для:
- управления подписками (CRUD);
- отображения перечня подписок;
- отображения аналитики расходов за выбранный период.
"""
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import SubscriptionForm
from utils import build_subscription

from storage import (
    create_subscription, 
    get_subscription, 
    get_subscriptions, 
    update_subscription, 
    delete_subscription
)
from analysis import (
    total_expenses,
    plot_category_pie,
    AnalyticsError
)

app = Flask(__name__)

@app.route("/")
def index():
    """
    Рендерит главную страницу с перечнем подписок.

    :returns: index.html
    """
    subs = []
    try:
        subs = get_subscriptions()
    except (ValueError, TypeError) as e:
        # Отправляем пользователю ошибку as is, т.к. 
        # для исправления ему нужен контекст
            flash(str(e), 'error')
    except RuntimeError as e:
        # Логируем ошибку БД для админа, но не показываем детали пользователю
        logging.exception('Не удалось получить подписки')
        flash('Не удалось получить подписки', 'error')

    return render_template('index.html', subscriptions=subs)


@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    """
    Обработчик создания новой подписки.

    GET:
        Рендерит пустую форму создания подписки.
    POST:
        Валидирует ввод и создаёт новую подписку.

    :returns: add_subscription.html
    """
    form = SubscriptionForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            create_subscription(build_subscription(form, None))
            return redirect(url_for('index'))
        except (ValueError, TypeError) as e:
            flash(str(e), 'error')
        except RuntimeError as e:
            logging.exception('Не удалось создать подписку')
            flash('Не удалось создать подписку', 'error')

    return render_template('add_subscription.html', form=form)


@app.route('/change-subscription/<string:id>', methods=['GET', 'POST'])
def change_subscription(id):
    """
    Редактирует существующую подписку, заменяя её данные на новые.
    По сути - PUT-метод.

    GET:
        Возвращает форму, предзаполненную данными подписки.
    POST:
        Валидирует ввод и обновляет подписку.

    :param sub_id: Идентификатор подписки
    :type sub_id: str

    :returns: change_subscription.html
    """
    form = SubscriptionForm(request.form)
    if request.method == 'GET':
        try:
            sub = get_subscription(id)
            form = SubscriptionForm(
                data={
                    'user': sub.user,
                    'title': sub.title,
                    'category': sub.category,
                    'start_date': sub.start_date.strftime('%Y-%m-%d'),
                    'end_date': sub.end_date.strftime('%Y-%m-%d'),
                    'price': sub.price,
                    'price_daily': sub.price_daily,
                    'descr': sub.descr
                }
            )
        except (ValueError, TypeError) as e:
            logging.exception('Не удалось получить подписку или она некорректна')
            flash(str(e), 'error')
        except RuntimeError as e:
            logging.exception('Не удалось получить подписку для редактирования')
            flash('Не удалось получить подписку для редактирования', 'error')
            return redirect(url_for('index'))

    if request.method == 'POST' and form.validate():
        try:
            update_subscription(build_subscription(form, id))
            return redirect(url_for('index'))
        except (ValueError, TypeError) as e:
            logging.exception('Не удалось обновить подписку')
            flash(str(e), 'error')
        except RuntimeError as e:
            logging.exception('Не удалось обновить подписку')
            flash('Не удалось обновить подписку', 'error')
            
    return render_template('change_subscription.html', form=form)


@app.route("/delete/<string:id>", methods=['POST'])
def del_subscription(id):
    """
    Удаляет подписку.

    :param sub_id: Идентификатор подписки
    :type sub_id: str
    :return: index.html
    """
    try:
        delete_subscription(id)
    except RuntimeError as e:
        logging.exception('Не удалось удалить подписку')
        flash('Не удалось удалить подписку', 'error')
    return redirect(url_for('index'))


@app.route("/analysis")
def analysis_page():
    """
    Отображает страницу аналитики.

    Принимает опциональные query-параметры:
    - start: дата начала периода (YYYY-MM-DD)
    - end: дата окончания периода (YYYY-MM-DD)

    :returns: analysis.html
    """
    start = request.args.get("start")
    end = request.args.get("end")

    total, category_chart = 0, None
    if not (start and end):
        return render_template("analysis.html", total=total)
    
    try:
        total=total_expenses(start, end)
        category_chart=plot_category_pie(start, end)
    except AnalyticsError as e:
        logging.exception('Не удалось построить аналитику')
        flash('Не удалось построить аналитику', 'error')
    
    return render_template(
        "analysis.html",
        start=start,
        end=end,
        total=total,
        category_chart=category_chart,
    )
