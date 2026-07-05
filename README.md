# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## System Design 
3 Core Actions User Should be able to Perform 
    1. Add basic owner and pet info 
    2. Adding or editing pet care tasks
    3. Generate and view daily care plan based on available time and task priority. 


## LISTING THE BUILDING BLOCKS 
Owner
- attributes: name, pets
- methods: add_pet(), get_pets()

Pet
- attributes: name, species, breed, age, tasks
- methods: add_task(), get_tasks()

Task
- attributes: name, category, duration, priority, preferred_time, recurring
- methods: mark_complete(), get_details()

CarePlan
- attributes: pet, available_time, scheduled_tasks
- methods: generate_plan(), sort_tasks(), get_plan()

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

##SAMPLE OUTPUT 
Today's Schedule
-----------------
09:00 - Biscuit: Breakfast (high priority)
08:00 - Biscuit: Morning Walk (high priority)
07:30 - Mochi: Clean Litter Box (medium priority)

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/rhearam/ai110-module2show-pawpal-starter
collected 13 items                                                             

tests/test_pawpal.py .....                                               [ 38%]
tests/test_pawpal_system.py ........                                     [100%]

============================== 13 passed in 0.01s ==============================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 🎬 Demo Walkthrough

The Streamlit app lets a user interact with the scheduling system in a simple, guided flow:

1. Add a pet by entering a name and species. The app stores the pet under the current owner.
2. Add care tasks for that pet, including a title, duration, priority, and preferred time.
3. Review the pending tasks in a structured table and see them grouped by pet.
4. Generate a schedule to view today's plan, which is sorted by preferred time and priority.
5. Review scheduler feedback such as conflict warnings when two tasks share the same time slot.

Example workflow:
- Add a pet such as "Mochi"
- Add a task like "Morning Walk" with a preferred time of 08:00
- Add another task like "Feed" at 09:00
- Generate the schedule to view the sorted daily plan

The scheduler demonstrates several core behaviors during this workflow:
- Sorting by time, then priority and duration
- Filtering out completed tasks when building the schedule
- Conflict warnings for overlapping task times
- Recurring-task support for daily or weekly care routines

Sample CLI output from running `main.py`:

```text
Today's Schedule
-----------------
07:30 - Mochi: Clean Litter Box (medium priority)
08:00 - Biscuit: Morning Walk (high priority)
09:00 - Biscuit: Breakfast (high priority)
```
