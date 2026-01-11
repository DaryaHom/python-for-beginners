"""
Транспортный уровень приложения. 

Модуль содержит роуты для:
- управления подписками (CRUD);
- отображения перечня подписок;
- отображения аналитики расходов за выбранный период.
"""

from flask import Flask, render_template, request, flash
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
    plot_category_pie
)

app = Flask(__name__)

@app.route("/")
def index():
    """
    Рендерит главную страницу с перечнем подписок.

    :return: index.html
    """
    try:
        subs = get_subscriptions()
    except RuntimeError as e:
        flash(str(e), 'error')

    return render_template('index.html', subscriptions=subs)


@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    """
    Обработчик создания новой подписки.

    GET:
        Рендерит пустую форму создания подписки.
    POST:
        Валидирует ввод и создаёт новую подписку.

    :return: add_subscription.html
    """
    form = SubscriptionForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            create_subscription(build_subscription(form, None))
            return index()
        except (ValueError, TypeError, RuntimeError) as e:
            flash(str(e), 'error')

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
    :return: change_subscription.html
    """
    form = SubscriptionForm(request.form)
    if request.method == 'GET':
        try:
            sub = get_subscription(id)
            form = SubscriptionForm(
                data={
                    'id': id,
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
        except RuntimeError as e:
            flash(f'Subscription not found {str(e)}', 'error')
            return index()

    if request.method == 'POST' and form.validate():
        try:
            update_subscription(build_subscription(form, id))
            return index()
        except (ValueError, TypeError) as e:
            flash(str(e), 'error')
            
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
        flash(f'Unable to delete subscription: {str(e)}', 'error')
    return index()


@app.route("/analysis")
def analysis_page():
    """
    Отображает страницу аналитики.

    Принимает опциональные query-параметры:
    - start: дата начала периода (YYYY-MM-DD)
    - end: дата окончания периода (YYYY-MM-DD)

    :return: analysis.html
    """
    start = request.args.get("start")
    end = request.args.get("end")

    if not (start and end):
        return render_template("analysis.html", total=0)
    
    return render_template(
        "analysis.html",
        start=start,
        end=end,
        total=total_expenses(start, end),
        category_chart=plot_category_pie(start, end),
    )
