from contextlib import nullcontext as does_not_raise
import pytest
from decimal import Decimal
from models import Subscription  


@pytest.mark.parametrize(
    "user, title, start_date, end_date, category, price, price_daily, id, descr, expectation",
    [
        (
            "alice", "Spotify Premium", "2025-01-01", "2026-01-01", "Музыка",
            Decimal("1190.00"), None, "123", "Best music app",
            does_not_raise()
        ),
        (
            "bob", "Netflix", "2025-06-15", "2025-09-15", "Видео и стриминг",
            None, Decimal("33.00"), None, "",
            does_not_raise()
        ),
        (
            "charlie", "Dropbox Pro", "2025-03-01", "2026-03-01", "Облачное хранилище",
            Decimal("1200.00"), Decimal("3.29"), "456789", "Cloud storage",
            does_not_raise()
        ),

        ("", "Spotify", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        (42, "Spotify", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, None, "", pytest.raises(TypeError)),
        ("alice", "", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", "", "2026-01-01", "Музыка", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", "2025-01-01", "", "Музыка", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", "2025-01-01", "2026-01-01", "", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        ("alice", "Spotify", "2025-01-01", "2026-01-01", 123, Decimal("100"), None, None, "", pytest.raises(TypeError)),
        ("alice", "FakeService", "2025-01-01", "2026-01-01", "Несуществующая категория", Decimal("100"), None, None, "", pytest.raises(ValueError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", None, None, None, "", pytest.raises(ValueError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", "100", None, None, "", pytest.raises(TypeError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", None, "5.50", None, "", pytest.raises(TypeError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, "abc", "", pytest.raises(ValueError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, "12a3", "", pytest.raises(ValueError)),
        ("alice", "Service", "2025-01-01", "2026-01-01", "Музыка", Decimal("100"), None, None, 123, pytest.raises(TypeError)),
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
    sub1 = Subscription(
        user="test",
        title="Test",
        start_date="2025-01-01",
        end_date="2025-01-11",  # 10 дней
        category="Музыка",
        price=None,
        price_daily=Decimal("10.00")
    )
    assert sub1.price == Decimal("100.00")  # 10 дней * 10

    # Если задан только price — price_daily вычисляется
    sub2 = Subscription(
        user="test",
        title="Test",
        start_date="2025-01-01",
        end_date="2025-01-11",  # 10 дней
        category="Музыка",
        price=Decimal("150.00"),
        price_daily=None
    )
    assert sub2.price_daily == Decimal("15.00")  # 150 / 10

    # Если end_date == start_date, не делить на ноль
    sub3 = Subscription(
        user="test",
        title="Test",
        start_date="2025-01-01",
        end_date="2025-01-01",
        category="Музыка",
        price=Decimal("50.00"),
        price_daily=None
    )
    assert sub3.price_daily == Decimal("50.00")  # полную цену

def test_subscription_descr_default():
    sub = Subscription(
        user="test",
        title="Test",
        start_date="2025-01-01",
        end_date="2025-02-01",
        category="Музыка",
        price=Decimal("100.00")
    )
    assert sub.descr == ''
