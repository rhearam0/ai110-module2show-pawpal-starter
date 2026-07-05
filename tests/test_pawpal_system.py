from datetime import date, timedelta

from pawpal_system import CarePlan, Owner, Pet, Scheduler, Task


def test_basic_model_structure():
    task = Task(
        name="Walk",
        category="exercise",
        duration=20,
        priority="high",
        preferred_time="morning",
        recurring=False,
    )
    pet = Pet(name="Mochi", species="dog", breed="Shiba", age=3)
    pet.add_task(task)

    owner = Owner(name="Jordan")
    owner.add_pet(pet)

    assert owner.get_pets() == [pet]
    assert pet.get_tasks() == [task]
    assert task.get_details()["name"] == "Walk"

    plan = CarePlan(pet=pet, available_time=60)
    plan.scheduled_tasks = [task]
    assert plan.generate_plan() == [task]
    assert plan.get_plan() == [task]


def test_task_completion():
    task = Task(name="Feed", category="meal", duration=5, priority="high")
    task.mark_complete()

    assert task.completed is True


def test_generate_plan_respects_available_time_and_priority():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", breed="Shiba", age=3)
    owner.add_pet(pet)

    high_priority_task = Task(name="Walk", category="exercise", duration=20, priority="high")
    low_priority_task = Task(name="Feed", category="meal", duration=15, priority="low")
    pet.add_task(high_priority_task)
    pet.add_task(low_priority_task)

    plan = CarePlan(owner=owner, pet=pet, available_time=25)
    scheduled = plan.generate_plan()

    assert plan.owner is owner
    assert scheduled == [high_priority_task]
    assert plan.get_plan() == [high_priority_task]


def test_duplicate_entries_are_ignored():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")

    owner.add_pet(pet)
    owner.add_pet(pet)

    pet.add_task(Task(name="Walk", duration=10))
    pet.add_task(Task(name="Walk", duration=10))

    assert owner.get_pets() == [pet]
    assert pet.get_tasks().count(pet.get_tasks()[0]) == 1


def test_scheduler_organizes_tasks_across_pets():
    owner = Owner(name="Jordan")
    pet_one = Pet(name="Mochi", species="dog")
    pet_two = Pet(name="Luna", species="cat")
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    walk = Task(name="Walk", duration=20, priority="high")
    feed = Task(name="Feed", duration=10, priority="low")
    litter = Task(name="Litter", duration=10, priority="medium")

    pet_one.add_task(walk)
    pet_one.add_task(feed)
    pet_two.add_task(litter)

    scheduler = Scheduler(owner=owner)
    all_tasks = scheduler.get_all_tasks()
    prioritized = scheduler.organize_tasks()

    assert len(all_tasks) == 3
    assert prioritized[0].name == "Walk"
    assert prioritized[-1].name == "Feed"


def test_scheduler_filters_by_pet_and_sorts_by_time():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task(name="Walk", duration=20, priority="high", preferred_time="08:00")
    feed = Task(name="Feed", duration=10, priority="medium", preferred_time="09:00")
    completed = Task(name="Brush", duration=10, priority="low", preferred_time="10:00")
    completed.mark_complete()

    dog.add_task(walk)
    dog.add_task(feed)
    dog.add_task(completed)

    litter = Task(name="Litter", duration=10, priority="medium", preferred_time="07:30")
    cat.add_task(litter)

    scheduler = Scheduler(owner=owner)
    dog_tasks = scheduler.organize_tasks(pet=dog, include_completed=False)

    assert [task.name for task in dog_tasks] == ["Walk", "Feed"]


def test_scheduler_keeps_recurring_tasks_and_detects_conflicts():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    walk = Task(name="Walk", duration=20, priority="high", preferred_time="08:00", recurring=True)
    feed = Task(name="Feed", duration=10, priority="medium", preferred_time="08:00")

    pet.add_task(walk)
    pet.add_task(feed)

    scheduler = Scheduler(owner=owner)
    recurring_tasks = scheduler.get_tasks(recurring_only=True, include_completed=False)
    conflicts = scheduler.detect_conflicts()

    assert [task.name for task in recurring_tasks] == ["Walk"]
    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feed" in conflicts[0]
    assert "Mochi" in conflicts[0]


def test_completed_daily_task_creates_next_occurrence():
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
