from contextlib import nullcontext as does_not_raise
import pytest

from decimal import Decimal
from task import Task, STATUS_COMPLETE
from employee import Employee

@pytest.mark.parametrize(
    "title, descr, status, employee, expectation",
    [
        ("new_task", 'easy task', 'Created', None, does_not_raise()), 
        ("new_task", '', 'Progress', Employee('Brian Hugh Warner', 'journalist', Decimal(100.0)), does_not_raise()), 
        
        ("new_task", '', 'Ok', None, pytest.raises(ValueError)), 
        ("new_task", '-', 'Complete', 42, pytest.raises(TypeError)),
    ]
)
def test_init_task(title, descr, status, employee, expectation):
    with expectation:
        assert Task(title, descr, status, employee) is not None
        
def test_assign_employee():
    t = Task("new_task", 'easy task')
    assert t.assign_employee(Employee('Brian Hugh Warner', 'journalist', Decimal(183.30), 42)) is None
    assert t.assigned_employee.name == 'Brian Hugh Warner'

def test_mark_complete():
    t = Task("new_task", 'easy task')
    assert t.mark_complete() is None
    assert t.status == STATUS_COMPLETE
