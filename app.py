from pawpal_system import Owner, Pet, Task, Scheduler

import streamlit as st

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered"
)

# Store the Owner object so it persists across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name}")

st.markdown("### Tasks")

pets = st.session_state.owner.get_pets()
selected_pet = None

if pets:
    selected_pet_name = st.selectbox("Choose a pet", [pet.name for pet in pets])
    selected_pet = next(pet for pet in pets if pet.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    preferred_time = st.text_input("Preferred time", value="08:00")

    if st.button("Add task"):
        new_task = Task(
            name=task_title,
            category="general",
            duration=int(duration),
            priority=priority,
            preferred_time=preferred_time,
            recurring=True,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' to {selected_pet.name}")

    st.write("Current pets and tasks:")
    scheduler = Scheduler(st.session_state.owner)
    for pet in pets:
        st.markdown(f"**{pet.name}** ({pet.species})")
        pending_tasks = scheduler.filter_tasks(tasks=pet.get_tasks(), include_completed=False)
        if pending_tasks:
            task_rows = [
                {
                    "Task": task.name,
                    "Time": task.preferred_time or "No time",
                    "Priority": task.priority,
                    "Duration": f"{task.duration} min",
                }
                for task in scheduler.organize_tasks(pet=pet, include_completed=False)
            ]
            st.table(task_rows)
        else:
            st.caption("No pending tasks yet.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    schedule = scheduler.organize_tasks(pet=selected_pet, include_completed=False)
    conflicts = scheduler.detect_conflicts()

    if conflicts:
        for warning in conflicts:
            st.warning(warning)

    if schedule:
        st.success("Schedule prepared for today.")
        st.markdown("### Today's Schedule")
        schedule_rows = [
            {
                "Task": task.name,
                "Time": task.preferred_time or "No time",
                "Priority": task.priority,
                "Duration": f"{task.duration} min",
            }
            for task in schedule
        ]
        st.table(schedule_rows)
    else:
        st.info("No pending tasks available to schedule.")