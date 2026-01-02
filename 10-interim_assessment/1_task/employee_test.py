# https://stackoverflow.com/questions/20274987/how-to-use-pytest-to-check-that-error-is-not-raised
from contextlib import nullcontext as does_not_raise
import pytest

from decimal import Decimal
from employee import Employee

@pytest.mark.parametrize(
    "name, pos, salary, hours, expectation",
    [
        ('Brian Hugh Warner', 'journalist', Decimal(100.0), 0, does_not_raise()), 
        ('Brian Hugh Warner', '-', Decimal(100.0), 160, does_not_raise()), 

        ('Brian Hugh Warner', '', Decimal(100.0), 160, pytest.raises(ValueError)), 
        (' ', '-', Decimal(100.0), 160, pytest.raises(ValueError)), 
        ('Brian Hugh Warner', 'journalist', Decimal(100.0), -160, pytest.raises(ValueError)),
        ('Brian Hugh Warner', 42, Decimal(100.0), 160, pytest.raises(TypeError)), 
        ('Brian Hugh Warner', 'journalist', 100.0, 160, pytest.raises(TypeError)), 
    ]
)
def test_init_project(name, pos, salary, hours, expectation):
    with expectation:
        assert Employee(name, pos, salary, hours) is not None


@pytest.mark.parametrize(
    "e, hours, wanted_hours, expectation",
    [
        (Employee('Brian Hugh Warner', 'journalist', Decimal(100.0)), 10, 10, does_not_raise()), 
        (Employee('Brian Hugh Warner', 'journalist', Decimal(100.0), 160), 40, 200, does_not_raise()), 

        (Employee('Brian Hugh Warner', 'journalist', Decimal(100.0)), -1, 0, pytest.raises(ValueError)), 
        (Employee('Brian Hugh Warner', 'journalist', Decimal(100.0)), '100', 0, pytest.raises(TypeError)), 
    ]
)
def test_add_hours(e, hours, wanted_hours, expectation):
    with expectation:
        assert e.add_hours(hours) is None
        assert e.hours_worked == wanted_hours

def test_calculate_pay():
    e = Employee('Brian Hugh Warner', 'journalist', Decimal(183.30), 42)
    assert e.calculate_pay() == Decimal('48.12')
