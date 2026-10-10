import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="StudyMate-AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 StudyMate-AI")
st.write("Your personal study planner and learning assistant.")

# File used to store tasks permanently
TASKS_FILE = Path(__file__).parent / "tasks.json"


def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(st.session_state.tasks, file, indent=4)


def load_tasks():
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
# Add a study task
st.subheader("📚 Add a Study Task")

with st.form("task_form"):
    subject = st.selectbox(
        "Choose your subject",
        ["Python", "Mathematics", "Computer Science", "AI"]
    )

    task = st.text_input("What do you want to study today?")

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task.strip():
            st.session_state.tasks.append({
                "subject": subject,
                "task": task.strip(),
                "completed": False
            })

            save_tasks()
            st.success("Task added successfully!")

        else:
            st.warning("Please enter a study task.")
# Display study tasks
# Display study tasks
st.subheader("📝 Your Study Tasks")

if len(st.session_state.tasks) == 0:
    st.info("No tasks yet. Add your first study task above!")

else:
    for i, item in enumerate(st.session_state.tasks):

        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:
            if item["completed"]:
                st.write(f"~~{item['task']}~~")
            else:
                st.write(f"**{item['task']}**")

            st.caption(f"Subject: {item['subject']}")

        with col2:
            button_label = "Undo" if item["completed"] else "Complete"

            if st.button(button_label, key=f"complete_{i}"):
                st.session_state.tasks[i]["completed"] = (
                    not st.session_state.tasks[i]["completed"]
                )

                save_tasks()
                st.rerun()

        with col3:
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)

                save_tasks()
                st.rerun()
                
# Progress dashboard
total = len(st.session_state.tasks)

completed = sum(
    1 for item in st.session_state.tasks
    if item["completed"]
)

remaining = total - completed

st.divider()
st.subheader("📊 Your Progress")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total)
col2.metric("Completed", completed)
col3.metric("Remaining", remaining)

if total > 0:
    st.progress(completed / total)
    # AI Study Assistant
st.divider()

st.header("🤖 AI Study Assistant")

st.write("Ask Gemini to help you understand difficult topics.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_question = st.text_input(
    "What would you like to learn today?",
    key="ai_question"
)

if st.button("Ask AI"):
    if user_question.strip():
        try:
            from google import genai

            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=(
                    "You are StudyMate-AI, a friendly study assistant. "
                    "Explain concepts in simple language for students.\n\n"
                    + user_question
                )
            )

            st.session_state.chat_history.append({
                "question": user_question,
                "answer": response.text
            })

        except Exception as e:
            st.error("Unable to get an AI response.")
            st.caption(str(e))

    else:
        st.warning("Please enter a question.")

for chat in reversed(st.session_state.chat_history):
    st.markdown("**🙋 Your question:**")
    st.write(chat["question"])

    st.markdown("**🤖 StudyMate-AI:**")
    st.write(chat["answer"])

    st.divider()