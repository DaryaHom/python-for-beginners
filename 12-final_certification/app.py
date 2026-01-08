from flask import Flask, render_template, request, flash

from forms import SubscriptionForm
from models import Subscription
from storage import save_subscription, get_subscriptions

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

