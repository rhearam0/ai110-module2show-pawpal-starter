from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    name: str
    category: str = "general"
    duration: int = 0
    priority: str = "medium"
    preferred_time: Optional[str] = None
    recurring: bool = False
    completed: bool = field(default=False, init=False)

    def mark_complete(self) -> None:
        self.completed = True

    def get_details(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "duration": self.duration,
            "priority": self.priority,
            "preferred_time": self.preferred_time,
            "recurring": self.recurring,
            "completed": self.completed,
        }


@dataclass
class Pet:
    """Represents a pet that can have many care tasks."""

    name: str
    species: str = "other"
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


@dataclass
class Owner:
    """Represents the pet owner and the pets they care for."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        return self.pets


@dataclass
class CarePlan:
    """Represents a generated care plan for a pet."""

    pet: Pet
    available_time: int = 0
    scheduled_tasks: List[Task] = field(default_factory=list)

    def generate_plan(self) -> List[Task]:
        return self.scheduled_tasks

    def sort_tasks(self) -> List[Task]:
        return sorted(
            self.scheduled_tasks,
            key=lambda task: (task.priority != "high", task.duration),
        )

    def get_plan(self) -> List[Task]:
        return self.scheduled_tasks
