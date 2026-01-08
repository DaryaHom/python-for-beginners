from flask import Flask, render_template, request, flash
from forms import SubscriptionForm
from models import Subscription

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


def build_subscription(form: SubscriptionForm, id: str | None = None) -> Subscription:
    """
    Build a Subscription domain object from a validated form.

    :param form: Validated subscription form
    :type form: SubscriptionForm
    :param id: Subscription identifier (None for new objects)
    :type id: str | None
    :return: Subscription entity
    :rtype: Subscription
    """
    return Subscription(
        id=id,
        user=form.user.data.strip(),
        title=form.title.data.strip(),
        start_date=form.start_date.data.strip(),
        end_date=form.end_date.data.strip(),
        category=form.category.data,
        price=form.price.data,
        price_daily=form.price_daily.data,
        descr=form.descr.data.strip(),
    )


@app.route("/")
def index():
    """
    Render the main page with the list of subscriptions.

    :return: Rendered index page
    """
    subs = get_subscriptions()
    return render_template('index.html', subscriptions=subs)


@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    """
    Handle subscription creation.

    GET:
        Render empty subscription form.
    POST:
        Validate input and persist new subscription.

    :return: Rendered page
    """
    form = SubscriptionForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            create_subscription(build_subscription(form, None))
            return index()
        except (ValueError, TypeError) as e:
            flash(str(e), 'error')

    return render_template('add_subscription.html', form=form)


@app.route('/change-subscription/<string:id>', methods=['GET', 'POST'])
def change_subscription(id):
    """
    Edit an existing subscription.

    GET:
        Pre-fill form with existing subscription data.
    POST:
        Update subscription after validation.

    :param sub_id: Subscription identifier
    :type sub_id: str
    :return: Rendered page
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
        except Exception as e:
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
    Delete a subscription.

    :param sub_id: Subscription identifier
    :type sub_id: str
    :return: Rendered index page
    """
    try:
        delete_subscription(id)
    except Exception as e:
        flash(f'Unable to delete subscription: {str(e)}', 'error')
    return index()


@app.route("/analysis")
def analysis_page():
    """
    Render analytics page.

    Accepts optional query parameters:
    - start: start date (YYYY-MM-DD)
    - end: end date (YYYY-MM-DD)

    :return: Rendered analytics page
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
