import pytest
from datetime import datetime
from decimal import Decimal

from contextlib import nullcontext as does_not_raise
from models import Subscription, PriceCalculator


@pytest.mark.parametrize(
    "user, title, start_date, end_date, category, price, price_daily, id, descr, expectation",
    [
        (
            "alice", "Spotify Premium", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка",
            Decimal("1190.00"), Decimal("1190.00"), "123", "Best music app",
            does_not_raise()
        ),
        (
            "bob", "Netflix", datetime(2023, 10, 5), datetime(2023, 10, 6), "Видео и стриминг",
            Decimal("33.00"), Decimal("33.00"), None, "",
            does_not_raise()
        ),
        (
            "charlie", "Dropbox Pro", datetime(2023, 10, 5), datetime(2023, 10, 9), "Облачное хранилище",
            Decimal("1200.00"), Decimal("300"), "456789", "Cloud storage",
            does_not_raise()
        ),

        ("", "Spotify", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), None, "", pytest.raises(ValueError)),
        (42, "Spotify", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), None, "", pytest.raises(TypeError)),
        ("alice", "", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", "", datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), None, "", pytest.raises(TypeError)),
        ("alice", "Spotify", datetime(2023, 10, 5), "", "Музыка", Decimal("100"), Decimal("100"), None, "", pytest.raises(TypeError)),
        ("alice", "Spotify", datetime(2023, 10, 5), datetime(2023, 10, 6), "", Decimal("100"), Decimal("100"), None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", datetime(2023, 10, 5), datetime(2023, 10, 6), 123, Decimal("100"), Decimal("100"), None, "", pytest.raises(TypeError)),
        ("alice", "FakeService", datetime(2023, 10, 5), datetime(2023, 10, 6), "Несуществующая категория", Decimal("100"), Decimal("100"), None, "", pytest.raises(ValueError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", None, None, None, "", pytest.raises(TypeError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", "100", None, None, "", pytest.raises(TypeError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", None, "5.50", None, "", pytest.raises(TypeError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), "abc", "", pytest.raises(ValueError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), "12a3", "", pytest.raises(ValueError)),
        ("alice", "Service", datetime(2023, 10, 5), datetime(2023, 10, 6), "Музыка", Decimal("100"), Decimal("100"), None, 123, pytest.raises(TypeError)),
    ]
)
def test_subscription_init(
    user, title, start_date, end_date, category, price, price_daily, id, descr, expectation
):
    with expectation:
        sub = Subscription(
            user=user,
            title=title,
            start_date=start_date,
            end_date=end_date,
            category=category,
            price=price,
            price_daily=price_daily,
            id=id,
            descr=descr
        )
        assert sub is not None


def test_subscription_price_calculation():
    # Если задан только price_daily — price вычисляется
    price, price_daily = PriceCalculator.calculate_price(
        start_date=datetime(2023, 10, 5),
        end_date=datetime(2023, 10, 15),  # 10 дней
        price=None,
        price_daily=Decimal("10.00")
    )
    assert price == Decimal("100.00")  # 10 дней * 10
    assert price_daily == Decimal("10.00")

    # Если задан только price — price_daily вычисляется
    price, price_daily = PriceCalculator.calculate_price(
        start_date=datetime(2023, 10, 5),
        end_date=datetime(2023, 10, 15),  # 10 дней
        price=Decimal("150.00"),
        price_daily=None
    )
    assert price == Decimal("150.00")
    assert price_daily == Decimal("15.00")  # 150 / 10

    # Если end_date == start_date, не делить на ноль
    price, price_daily = PriceCalculator.calculate_price(
        start_date=datetime(2023, 10, 5),
        end_date=datetime(2023, 10, 5),
        price=Decimal("50.00"),
        price_daily=None
    )
    assert price_daily == Decimal("50.00")  # полную цену
