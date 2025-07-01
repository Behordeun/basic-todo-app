import streamlit as st
from datetime import datetime, date

st.set_page_config(page_title="📅 To-Do App", layout="wide")
st.title("🌟 My To-Do List")

# --- Session State Initialization ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "show_completed" not in st.session_state:
    st.session_state.show_completed = True

# --- Task Entry Form ---
with st.container():
    with st.form(key="add_task_form", clear_on_submit=True):
        st.subheader("➕ Add a New Task")
        task_text = st.text_input("What's on your mind?", placeholder="e.g., Finish assignment")
        task_due = st.date_input("Set a due date", min_value=date.today())
        submitted = st.form_submit_button("Add", use_container_width=True)
        if submitted and task_text.strip():
            st.session_state.tasks.append({
                "task": task_text.strip(),
                "done": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "due_date": task_due.strftime("%Y-%m-%d")
            })

# --- Sidebar Options ---
with st.sidebar:
    st.markdown("## ⚙️ Options")
    st.session_state.show_completed = st.checkbox(
        "Show Completed Tasks", value=st.session_state.show_completed
    )
    if st.button("🧹 Clear All Tasks", use_container_width=True):
        st.session_state.tasks.clear()
        st.success("Tasks cleared!")

# --- Task Display Grouped by Due Date ---
st.subheader("📋 Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above!")
else:
    tasks_sorted = sorted(st.session_state.tasks, key=lambda x: x["due_date"])
    grouped_tasks = {}
    for task in tasks_sorted:
        grouped_tasks.setdefault(task["due_date"], []).append(task)

    for due_date, task_group in grouped_tasks.items():
        due_label = f"📅 {due_date}"
        if due_date == date.today().strftime("%Y-%m-%d"):
            due_label += " – **Today**"
        elif date.fromisoformat(due_date) < date.today():
            due_label += " – 🔴 **Overdue**"

        st.markdown(f"### {due_label}")

        for i, task in enumerate(task_group):
            global_index = st.session_state.tasks.index(task)
            if not st.session_state.show_completed and task["done"]:
                continue

            cols = st.columns([0.07, 0.7, 0.13, 0.1])
            done = cols[0].checkbox("", value=task["done"], key=f"done_{global_index}")
            st.session_state.tasks[global_index]["done"] = done

            text = f"✅ ~~{task['task']}~~" if done else f"🔹 {task['task']}"
            created = f"<span style='color:gray;font-size:10px;'>🕒 {task['created_at']}</span>"
            due = f"<span style='color:gray;font-size:10px;'>📆 Due: {task['due_date']}</span>"
            cols[1].markdown(f"{text}<br>{created}<br>{due}", unsafe_allow_html=True)

            if cols[2].button("✏️", key=f"edit_{global_index}"):
                new_value = st.text_input("Edit Task", task["task"], key=f"edit_input_{global_index}")
                st.session_state.tasks[global_index]["task"] = new_value

            if cols[3].button("❌", key=f"del_{global_index}"):
                st.session_state.tasks.pop(global_index)
                st.experimental_rerun()
