
import streamlit as st
import json
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="StudyMate-AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM LAVENDER CSS ----------------
# ---------------- CUSTOM LAVENDER CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #faf8ff 0%, #f1ebff 100%);
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3, h4 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #39265c !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px;
}

p, label, .stMarkdown, .stCaption {
    font-family: 'Inter', sans-serif;
    color: #514365;
}

.hero {
    background: linear-gradient(120deg, #7550c9, #a78bfa);
    padding: 35px;
    border-radius: 24px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(117, 80, 201, 0.15);
}

.hero h1 {
    color: white !important;
    font-size: 2.7rem !important;
    margin-bottom: 8px;
}

.hero p {
    color: #f5f0ff !important;
    font-size: 1.05rem;
    line-height: 1.8;
}

.eyebrow {
    color: #eee5ff;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.88);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e8defb;
    box-shadow: 0 5px 18px rgba(73, 46, 115, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #786692;
}

div[data-testid="stMetricValue"] {
    color: #6941c6;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: #7950d9;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #6037b7;
    color: white;
    transform: translateY(-2px);
}

input, textarea {
    font-family: 'Inter', sans-serif !important;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 12px;
    border-color: #d9cafa;
    background-color: white;
}

.stProgress > div > div > div > div {
    background-color: #8b5cf6;
}

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #e8defb;
    padding: 22px;
    border-radius: 18px;
}

.task-title {
    color: #39265c;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
}

.task-subject {
    color: #8b78a8;
    font-size: 0.82rem;
    margin-top: 5px;
}

.assistant-card {
    background: linear-gradient(135deg, #ffffff, #f5efff);
    border: 1px solid #e4d7fc;
    border-radius: 20px;
    padding: 22px;
    margin: 10px 0 20px 0;
}

div[data-testid="stSidebar"] {
    background: #f1eaff;
    border-right: 1px solid #e3d6fb;
}

div[data-testid="stSidebar"] * {
    color: #493568;
}

hr {
    border-color: #e6dcf8;
}

footer, #MainMenu {
    visibility: hidden;
}
/* Fix text visibility in input boxes */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #39265c !important;
    -webkit-text-fill-color: #39265c !important;
    border: 1px solid #d9cafa !important;
}

/* Make placeholder text visible */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9b8bb8 !important;
    -webkit-text-fill-color: #9b8bb8 !important;
    opacity: 1 !important;
}

/* Ensure input labels are readable */
.stTextInput label,
.stTextArea label {
    color: #39265c !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA STORAGE ----------------

TASKS_FILE = Path(__file__).parent / "tasks.json"


def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(st.session_state.tasks, file, indent=4)


def load_tasks():
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                tasks = json.load(file)

            if isinstance(tasks, list):
                return [
                    item for item in tasks
                    if isinstance(item, dict)
                    and "task" in item
                    and "subject" in item
                ]

        except (json.JSONDecodeError, OSError):
            pass

    return []


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🎓 StudyMate")
    st.caption("YOUR PERSONAL STUDY SPACE")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["🏠 Dashboard", "📚 Study Planner", "🤖 AI Assistant"]
    )

    st.divider()
    st.markdown("### ✨ Your study journey")
    st.write("Small steps every day lead to big achievements.")
    st.caption("Made with 💜 for curious minds.")


# ---------------- DASHBOARD HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR PERSONAL LEARNING SPACE</div>
    <h1>Welcome to StudyMate! 💜</h1>
    <p>Plan your day, track your progress, and make learning easier.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- PROGRESS CALCULATIONS ----------------

total = len(st.session_state.tasks)

completed = sum(
    1 for item in st.session_state.tasks
    if item.get("completed", False)
)

remaining = total - completed

progress = completed / total if total else 0


# ---------------- DASHBOARD PAGE ----------------

if page == "🏠 Dashboard":

    st.subheader("📊 Your Study Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("📚 Total Tasks", total)
    col2.metric("✅ Completed", completed)
    col3.metric("🌱 Remaining", remaining)

    st.markdown("### 🌷 Your progress")

    st.progress(progress)

    st.caption(
        f"You have completed {round(progress * 100)}% of your study tasks."
        if total
        else "Add your first task to begin your study journey!"
    )

    st.divider()

    st.subheader("📝 Upcoming Study Tasks")

    if not st.session_state.tasks:
        st.info(
            "Your study space is waiting for you! "
            "Head to Study Planner to add your first task. 💜"
        )
    else:
        for i, item in enumerate(st.session_state.tasks):
            if item.get("completed", False):
                continue

            with st.container(border=True):
                col1, col2 = st.columns([5, 1])

                with col1:
                    st.markdown(f"**{item['task']}**")
                    st.caption(f"📚 {item['subject']}")

                with col2:
                    if st.button("Complete", key=f"dash_complete_{i}"):
                        st.session_state.tasks[i]["completed"] = True
                        save_tasks()
                        st.rerun()

    st.divider()

    st.markdown("""
    <div class="assistant-card">
        <h3>🤖 Need help with a difficult topic?</h3>
        <p>Visit your AI Assistant to explore concepts and get simple explanations.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- STUDY PLANNER PAGE ----------------

elif page == "📚 Study Planner":

    st.subheader("📚 Plan your learning")

    st.write("Add a task, work through it, and celebrate your progress!")

    with st.form("task_form", clear_on_submit=True):

        subject = st.selectbox(
            "Choose your subject",
            ["Python", "Mathematics", "Computer Science", "AI"]
        )

        task = st.text_input(
            "What do you want to study?",
            placeholder="e.g. Practice Python functions"
        )

        submitted = st.form_submit_button(
            "➕ Add Study Task",
            use_container_width=True
        )

        if submitted:
            if task.strip():

                st.session_state.tasks.append({
                    "subject": subject,
                    "task": task.strip(),
                    "completed": False
                })

                save_tasks()
                st.success("Your new study task has been added! 🎉")
                st.rerun()

            else:
                st.warning("Please enter a task first.")

    st.divider()

    st.subheader("📝 Your tasks")

    if not st.session_state.tasks:
        st.info("No tasks yet. Add your first study task above!")
    else:
        for i, item in enumerate(st.session_state.tasks):

            with st.container(border=True):

                col1, col2, col3 = st.columns([5, 1.5, 1])

                with col1:
                    if item.get("completed", False):
                        st.markdown(f"~~{item['task']}~~")
                        st.caption(f"✅ {item['subject']} · Completed")
                    else:
                        st.markdown(f"**{item['task']}**")
                        st.caption(f"📚 {item['subject']}")

                with col2:
                    label = (
                        "↩️ Undo"
                        if item.get("completed", False)
                        else "✅ Complete"
                    )

                    if st.button(label, key=f"planner_complete_{i}"):
                        st.session_state.tasks[i]["completed"] = (
                            not item.get("completed", False)
                        )

                        save_tasks()
                        st.rerun()

                with col3:
                    if st.button("🗑️", key=f"planner_delete_{i}"):
                        st.session_state.tasks.pop(i)
                        save_tasks()
                        st.rerun()


# ---------------- AI ASSISTANT PAGE ----------------

elif page == "🤖 AI Assistant":

    st.subheader("🤖 Meet your AI Study Assistant")

    st.write(
        "Ask questions about Python, mathematics, computer science, "
        "AI, or any topic you want to understand."
    )

    st.markdown("""
    <div class="assistant-card">
        <h3>💜 Curious about something?</h3>
        <p>Ask away! StudyMate will help explain concepts in student-friendly language.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("ai_form", clear_on_submit=True):
        user_question = st.text_input(
            "Your question",
            placeholder="e.g. Explain Python virtual environments simply..."
        )

        ask = st.form_submit_button(
            "✨ Ask StudyMate",
            use_container_width=True
        )

    if ask:

        if user_question.strip():

            try:
                from google import genai

                client = genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=(
                        "You are StudyMate-AI, a friendly study assistant. "
                        "Explain concepts in simple language for students. "
                        "Use examples when helpful.\n\n"
                        + user_question.strip()
                    )
                )

                if response.text:
                    st.session_state.chat_history.append({
                        "question": user_question.strip(),
                        "answer": response.text
                    })
                    st.rerun()
                else:
                    st.warning(
                        "The AI returned an empty response. Try again."
                    )

            except Exception as e:
                st.error(f"Gemini API error: {e}")

        else:
            st.warning("Please enter a question first.")

    if st.session_state.chat_history:

        st.divider()
        st.subheader("💬 Your conversation")

        for chat in reversed(st.session_state.chat_history):

            with st.container(border=True):
                st.markdown("**🙋 You asked**")
                st.write(chat["question"])

                st.markdown("**🤖 StudyMate answered**")
                st.write(chat["answer"])


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<p style='text-align:center;color:#8b78a8;'>"
    "Made with 💜 · StudyMate-AI · Your journey, your pace."
    "</p>",
     unsafe_allow_html=True)
