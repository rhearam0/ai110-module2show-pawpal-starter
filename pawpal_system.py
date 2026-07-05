from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


def _time_to_minutes(value: Optional[str]) -> int:
    """Convert a time string like 08:00 into minutes since midnight."""
    if not value:
        return 24 * 60
    try:
        hours, minutes = value.split(":")
        return int(hours) * 60 + int(minutes)
    except ValueError:
        return 24 * 60


@dataclass
class Task:
    """Represents a single activity for a pet care routine."""

    name: str
    category: str = "general"
    duration: int = 0
    priority: str = "medium"
    preferred_time: Optional[str] = None
    recurring: bool = False
    recurrence_interval: Optional[str] = None
    due_date: Optional[date] = None
    completed: bool = field(default=False, init=False)

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and create the next recurring occurrence if needed."""
        self.completed = True

        if not self.recurring:
            return None

        if self.recurrence_interval == "daily":
            next_due_date = date.today() + timedelta(days=1)
        elif self.recurrence_interval == "weekly":
            next_due_date = date.today() + timedelta(days=7)
        else:
            next_due_date = date.today()

        return Task(
            name=self.name,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            preferred_time=self.preferred_time,
            recurring=self.recurring,
            recurrence_interval=self.recurrence_interval,
            due_date=next_due_date,
        )

    def get_details(self) -> dict:
        """Return a dictionary describing the task."""
        return {
            "name": self.name,
            "category": self.category,
            "duration": self.duration,
            "priority": self.priority,
            "preferred_time": self.preferred_time,
            "recurring": self.recurring,
            "recurrence_interval": self.recurrence_interval,
            "due_date": self.due_date,
            "completed": self.completed,
        }


@dataclass
class Pet:
    """Stores pet details and the tasks associated with that pet."""

    name: str
    species: str = "other"
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet if it is not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to the pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manages one or more pets and exposes their tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner if it is not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by the owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets owned by the owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


@dataclass
class Scheduler:
    """The brain of the system that retrieves and organizes tasks across pets."""

    owner: Optional[Owner] = None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from the owner’s pets."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks()

    def get_tasks(
        self,
        pet: Optional[Pet] = None,
        recurring_only: bool = False,
        include_completed: bool = True,
    ) -> List[Task]:
        """Return tasks optionally filtered by pet, recurrence, and completion status."""
        tasks = self.get_all_tasks()
        if pet is not None:
            tasks = [task for task in tasks if task in pet.get_tasks()]
        if recurring_only:
            tasks = [task for task in tasks if task.recurring]
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks

    def organize_tasks(
        self,
        pet: Optional[Pet] = None,
        include_completed: bool = True,
    ) -> List[Task]:
        """Sort tasks by preferred time, then priority, and duration for scheduling."""
        tasks = self.get_tasks(pet=pet, include_completed=include_completed)

        def task_sort_key(task: Task) -> tuple[int, int, int, str]:
            return (
                _time_to_minutes(task.preferred_time),
                -self._priority_rank(task.priority),
                task.duration,
                task.name.lower(),
            )

        return sorted(tasks, key=task_sort_key)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return a chronologically ordered list of tasks by preferred time.

        The preferred_time value is converted to minutes since midnight so
        times like "08:00" and "14:30" sort correctly.
        """
        return sorted(
            tasks,
            key=lambda task: _time_to_minutes(task.preferred_time),
        )

    def filter_tasks(
        self,
        tasks: Optional[List[Task]] = None,
        pet_name: Optional[str] = None,
        include_completed: Optional[bool] = None,
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status.

        If a pet name is provided, only tasks belonging to that pet are kept.
        If include_completed is set, tasks are filtered to match that state.
        """
        candidate_tasks = list(tasks if tasks is not None else self.get_all_tasks())

        if pet_name is not None:
            candidate_tasks = [
                task for task in candidate_tasks
                if any(pet.name.lower() == pet_name.lower() for pet in self.owner.get_pets() if task in pet.get_tasks())
            ]

        if include_completed is not None:
            candidate_tasks = [task for task in candidate_tasks if task.completed is include_completed]

        return candidate_tasks

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and add the next recurring instance to its pet.

        If the task is recurring, a new task instance is created and attached to
        the pet that currently owns the completed task.
        """
        next_task = task.mark_complete()
        if next_task is None or self.owner is None:
            return next_task

        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                pet.add_task(next_task)
                break

        return next_task

    def detect_conflicts(self) -> List[str]:
        """Return lightweight warning messages for overlapping task times.

        Tasks that share the same preferred_time are treated as potential
        conflicts, and a readable warning is returned instead of raising an error.
        """
        warnings: List[str] = []
        if self.owner is None:
            return warnings

        tasks = [task for task in self.get_all_tasks() if not task.completed and task.preferred_time]
        seen_pairs = set()

        for index, task in enumerate(tasks):
            for other in tasks[index + 1 :]:
                try:
                    if _time_to_minutes(task.preferred_time) != _time_to_minutes(other.preferred_time):
                        continue
                except (TypeError, ValueError):
                    continue

                pair_key = tuple(sorted((id(task), id(other))))
                if pair_key in seen_pairs:
                    continue

                seen_pairs.add(pair_key)
                task_pet = self._find_pet_name(task)
                other_pet = self._find_pet_name(other)

                if task_pet and other_pet and task_pet == other_pet:
                    warnings.append(
                        f"Warning: '{task.name}' and '{other.name}' overlap at {task.preferred_time} for {task_pet}."
                    )
                else:
                    warnings.append(
                        f"Warning: '{task.name}' and '{other.name}' overlap at {task.preferred_time}."
                    )

        return warnings

    def _find_pet_name(self, task: Task) -> Optional[str]:
        """Return the pet name that owns the given task, if it exists."""
        if self.owner is None:
            return None

        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                return pet.name

        return None

    def _priority_rank(self, priority: str) -> int:
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(priority.lower(), 0)


@dataclass
class CarePlan:
    """Represents a generated care plan for a pet."""

    owner: Optional[Owner] = None
    pet: Optional[Pet] = None
    available_time: int = 0
    scheduled_tasks: List[Task] = field(default_factory=list)

    def _priority_rank(self, priority: str) -> int:
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(priority.lower(), 0)

    def generate_plan(self) -> List[Task]:
        """Build a simple task plan within the available time."""
        if self.pet is None or self.available_time <= 0:
            self.scheduled_tasks = []
            return self.scheduled_tasks

        selected_tasks: List[Task] = []
        remaining_time = self.available_time

        for task in sorted(
            self.pet.get_tasks(),
            key=lambda item: (-self._priority_rank(item.priority), item.duration),
        ):
            if task.completed:
                continue
            if task.duration <= remaining_time:
                selected_tasks.append(task)
                remaining_time -= task.duration

        self.scheduled_tasks = selected_tasks
        return self.scheduled_tasks

    def sort_tasks(self) -> List[Task]:
        """Return the scheduled tasks sorted by priority and duration."""
        return sorted(
            self.scheduled_tasks,
            key=lambda task: (-self._priority_rank(task.priority), task.duration),
        )

    def get_plan(self) -> List[Task]:
        """Return the currently scheduled tasks."""
        return self.scheduled_tasks
