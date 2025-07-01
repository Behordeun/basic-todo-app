import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📝 To-Do App", layout="wide")
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
        task_text = st.text_input(
            "What's on your mind?",
            key="input_task",
            placeholder="e.g., Schedule a meeting",
        )
        submitted = st.form_submit_button("Add", use_container_width=True)
        if submitted and task_text.strip():
            st.session_state.tasks.append({
                "task": task_text.strip(),
                "done": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
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

# --- Task List Display ---
st.subheader("📋 Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above!")
else:
    for i, task in enumerate(st.session_state.tasks):
        if not st.session_state.show_completed and task["done"]:
            continue

        cols = st.columns([0.07, 0.73, 0.1, 0.1])
        done = cols[0].checkbox("", value=task["done"], key=f"done_{i}")
        st.session_state.tasks[i]["done"] = done

        display_text = f"✅ ~~{task['task']}~~" if done else f"🔹 {task['task']}"
        cols[1].markdown(display_text + f"<br><span style='color:gray;font-size:10px;'>🕒 {task['created_at']}</span>", unsafe_allow_html=True)

        if cols[2].button("✏️", key=f"edit_{i}"):
            new_value = st.text_input("Edit Task", task["task"], key=f"edit_input_{i}")
            st.session_state.tasks[i]["task"] = new_value

        if cols[3].button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
