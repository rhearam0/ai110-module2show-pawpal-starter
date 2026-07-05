from pawpal_system import Owner, Pet, Scheduler, Task

# Create an owner
owner = Owner("Rhea")

# Create two pets
dog = Pet("Biscuit", "Dog", "Golden Retriever", 3)
cat = Pet("Mochi", "Cat", "Tabby", 2)

# Create tasks
walk = Task(
    name="Morning Walk",
    category="Exercise",
    duration=30,
    priority="high",
    preferred_time="08:00",
    recurring=True
)

feed = Task(
    name="Breakfast",
    category="Feeding",
    duration=10,
    priority="high",
    preferred_time="09:00",
    recurring=True
)

litter = Task(
    name="Clean Litter Box",
    category="Cleaning",
    duration=15,
    priority="medium",
    preferred_time="07:30",
    recurring=True
)

# Add tasks to pets
dog.add_task(walk)
cat.add_task(litter)
dog.add_task(feed)


# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create the scheduler and use it to organize tasks
scheduler = Scheduler(owner=owner)
organized_tasks = scheduler.organize_tasks()

# Print today's schedule
print("Today's Schedule")
print("-----------------")

for task in organized_tasks:
    pet_name = next(
        (pet.name for pet in owner.get_pets() if task in pet.get_tasks()),
        "Unknown",
    )
    print(f"{task.preferred_time} - {pet_name}: {task.name} ({task.priority} priority)")