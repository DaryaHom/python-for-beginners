from flask import Flask, render_template, request, flash

from forms import SubscriptionForm
from models import Subscription
from storage import (
    save_subscription, 
    get_subscription, 
    get_subscriptions, 
    update_subscription, 
    delete_subscription
)
from analysis import (
    total_expenses,
    expenses_by_category,
    plot_category_pie
)

app = Flask(__name__)

@app.route("/")
def index():
    subs = get_subscriptions()
    return render_template('index.html', subscriptions=subs)

@app.route('/add-subscription', methods=['GET', 'POST'])
def add_subscription():
    form = SubscriptionForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            sub = Subscription(
                id=None,
                user=form.user.data.strip(),
                title=form.title.data.strip(),
                start_date=form.start_date.data.strip(),
                end_date=form.end_date.data.strip(),
                category=form.category.data,
                price=form.price.data,
                price_daily=form.price_daily.data,
                descr=form.descr.data.strip() if form.descr.data else ''
            )
            save_subscription(sub)
            return render_template('index.html', subscriptions=get_subscriptions())
        except (ValueError, TypeError) as e:
            flash(str(e), 'error')

    return render_template('add_subscription.html', form=form)

@app.route('/change-subscription/<string:id>', methods=['GET', 'POST'])
def change_subscription(id):
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
        except:
            pass # TODO

    if request.method == 'POST' and form.validate():
        try:
            sub = Subscription(
                id=id,
                user=form.user.data.strip(),
                title=form.title.data.strip(),
                start_date=form.start_date.data.strip(),
                end_date=form.end_date.data.strip(),
                category=form.category.data,
                price=form.price.data,
                price_daily=form.price_daily.data,
                descr=form.descr.data.strip() if form.descr.data else ''
            )
            update_subscription(sub)
            return render_template('index.html', subscriptions=get_subscriptions())
        except (ValueError, TypeError) as e:
            flash(str(e), 'error')
            
    return render_template('change_subscription.html', form=form)

@app.route("/delete/<string:id>", methods=['POST'])
def del_subscription(id):
    try:
        delete_subscription(id)
    except:
        pass #TODO
    subs = get_subscriptions()
    return render_template('index.html', subscriptions=subs)

@app.route("/analysis")
def analysis_page():
    start = request.args.get("start")
    end = request.args.get("end")

    if start and end:
        total = total_expenses(start, end)
        category_chart = plot_category_pie(start, end)

        return render_template(
            "analysis.html",
            total=total,
            category_chart=category_chart,
            start=start,
            end=end
        )
    return render_template(
            "analysis.html",
            total= 0
        )

