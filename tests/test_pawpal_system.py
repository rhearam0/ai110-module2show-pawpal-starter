from pawpal_system import CarePlan, Owner, Pet, Task


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
