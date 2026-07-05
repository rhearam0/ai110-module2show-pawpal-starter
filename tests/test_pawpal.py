from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_marks_task_as_complete():
    task = Task(name="Morning Walk", duration=20, priority="high")

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    task = Task(name="Feed", duration=10, priority="medium")

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_scheduler_returns_tasks_in_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    late_task = Task(name="Dinner", duration=10, priority="medium", preferred_time="19:00")
    early_task = Task(name="Breakfast", duration=10, priority="high", preferred_time="07:30")
    mid_task = Task(name="Walk", duration=20, priority="high", preferred_time="12:00")

    pet.add_task(late_task)
    pet.add_task(early_task)
    pet.add_task(mid_task)

    scheduler = Scheduler(owner=owner)
    ordered_tasks = scheduler.sort_by_time([late_task, early_task, mid_task])

    assert [task.name for task in ordered_tasks] == ["Breakfast", "Walk", "Dinner"]


def test_marking_daily_task_complete_creates_next_day_occurrence():
    task = Task(
        name="Feed",
        duration=10,
        priority="high",
        preferred_time="08:00",
        recurring=True,
        recurrence_interval="daily",
        due_date=date.today(),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.name == "Feed"
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.recurring is True


def test_scheduler_detects_conflicts_for_duplicate_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    first_task = Task(name="Walk", duration=20, priority="high", preferred_time="08:00")
    second_task = Task(name="Feed", duration=10, priority="medium", preferred_time="08:00")

    pet.add_task(first_task)
    pet.add_task(second_task)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feed" in conflicts[0]
    assert "Mochi" in conflicts[0]
