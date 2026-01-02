from contextlib import nullcontext as does_not_raise
import pytest

from project import Project
from task import Task, STATUS_PROGRESS, STATUS_COMPLETE

@pytest.mark.parametrize(
    "title, tasks, expectation",
    [
        ("new_project", [], does_not_raise()),
        ("new_project", [Task('task_1')], does_not_raise()),
        ("new_project", [Task('task_1'), Task('task_2')], does_not_raise()),

        ("  ", [], pytest.raises(ValueError)),
        (42, [], pytest.raises(TypeError)),
    ]
)
def test_init_project(title, tasks, expectation):
    with expectation:
        assert Project(title, tasks) is not None

def test_add_task():
    p = Project("new_project", None)
    assert p.add_task(Task("new_task", 'easy task')) is None
    assert len(p.tasks) == 1

def test_project_progress():
    p = Project("new_project")
    p.add_task(Task("new_task", 'easy task'))
    p.add_task(Task("new_task", 'middle task', STATUS_PROGRESS))
    p.add_task(Task("new_task", 'hard task', STATUS_COMPLETE))

    assert p.project_progress() == 33.33
    assert len(p.tasks) == 3
