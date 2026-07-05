from pawpal_system import Pet, Task


def test_task_completion_marks_task_as_complete():
    task = Task(name="Morning Walk", duration=20, priority="high")

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    task = Task(name="Feed", duration=10, priority="medium")

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1
