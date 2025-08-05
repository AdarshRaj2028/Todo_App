# ───────────────────────────────────────────────────────────────────────────
# 📒  QUICK-REFERENCE COMMENTS FOR THE HTML + CSS USED IN THIS FILE
# ───────────────────────────────────────────────────────────────────────────
#
# ╭──────────────────────── 1. BASIC HTML IN STREAMLIT ─────────────────────╮
# | • st.markdown() accepts raw HTML when unsafe_allow_html=True.           |
# | • We inject headings <h1> and paragraphs <p> for richer formatting.     |
# | • Example:                                                              |
# |     st.markdown('<h1 class="main-header">Title</h1>', unsafe_allow_html=True)|
# |   – class="main-header" lets us style it later in CSS.                  |
# ╰──────────────────────────────────────────────────────────────────────────╯
#
# ╭──────────────────────── 2. CSS SELECTORS WE USE  ───────────────────────╮
# | .main-header           → Any tag with class="main-header"               |
# | .subtitle              → Same idea for the subtitle paragraph           |
# | .todo-container        → Wrapper <div> around the active-task section   |
# | .completed-container   → Wrapper <div> around the completed-task section|
# | .stTextInput … input   → Deep selector that reaches Streamlit’s <input> |
# |                           element to round its corners.                 |
# | .stButton > button     → Targets the native <button> inside each        |
# |                           Streamlit button component.                   |
# ╰──────────────────────────────────────────────────────────────────────────╯
#
# ╭──────────────────────── 3. CSS PROPERTIES AT A GLANCE ──────────────────╮
# | background-color       • Solid background colour                        |
# | padding                • Inner spacing (like “internal margin”)         |
# | border / border-radius • Border line & corner roundness                 |
# | margin-bottom          • Space *below* an element                       |
# | color                  • Text colour                                    |
# | linear-gradient()      • Smooth colour transition (button bg)           |
# | transform: translateY  • Vertical move—used for hover “lift” effect     |
# | transition             • Animates property changes (smooth hover)       |
# ╰──────────────────────────────────────────────────────────────────────────╯
#
# ╭─────────────── 4. GOOD-PRACTICE REMINDERS FOR YOUR OWN CSS ─────────────╮
# | ①  Keep class names descriptive (e.g., .todo-container)                 |
# | ②  Prefer classes over IDs unless you truly need a single element.      |
# | ③  Group related rules; put global colours/fonts at the top.            |
# | ④  Use rem / % for spacing when possible to stay responsive.            |
# | ⑤  Avoid !important unless it’s truly necessary.                        |
# | ⑥  Test hover/active states in both light & dark themes.                |
# | ⑦  Keep custom CSS inside ONE st.markdown() block to avoid duplicates.  |
# ╰──────────────────────────────────────────────────────────────────────────╯
#
# ╭──────────────────────── 5. STREAMLIT DOM NOTE  ─────────────────────────╮
# | Streamlit wraps every element in its own <div>. Our deep selectors      |
# | (.stTextInput > div > div > input) drill through those layers. If a     |
# | future Streamlit release changes its internal DOM, re-test your CSS.    |
# ╰──────────────────────────────────────────────────────────────────────────╯
#
# ╭──────────────────────── 6. WHY WE CENTER THE INPUT ─────────────────────╮
# | • `left_spacer, center, right_spacer = st.columns([1, 2, 1])`           |
# |   creates a 3-column grid with a 1 : 2 : 1 width ratio.                 |
# | • Putting the text_input in the middle column visually centres it.      |
# | • `label_visibility='collapsed'` hides the (empty) label row.           |
# ╰──────────────────────────────────────────────────────────────────────────╯


# ────────────────────────────── PYTHON CODE BELOW ──────────────────────────
import streamlit as st
import os
import functions  # your own helper module


# -------- FILE-SYSTEM SET-UP ------------------------------------------------
APPDATA_DIR = os.path.join(os.path.expanduser("~"), ".todo_app")  # hidden dir in user’s home
os.makedirs(APPDATA_DIR, exist_ok=True)

FILEPATH_TODO      = os.path.join(APPDATA_DIR, "todo_list.txt")
FILEPATH_COMPLETED = os.path.join(APPDATA_DIR, "completed_todo_list.txt")

# create empty files the first time the app runs
if not os.path.isfile(FILEPATH_TODO):
    open(FILEPATH_TODO, "w").close()
if not os.path.isfile(FILEPATH_COMPLETED):
    open(FILEPATH_COMPLETED, "w").close()


# -------- CALLBACKS --------------------------------------------------------
def add_todo() -> None:
    """
    Called automatically when the user presses Enter in the text_input.
    Adds a new todo and lets Streamlit rerun the script implicitly.
    """
    todos = st.session_state["new_todo"].strip()
    if todos:
        # always read the file again to get the freshest list
        todo_list = functions.load_todos(FILEPATH_TODO)
        functions.add(todos, todo_list)
        st.session_state["new_todo"] = ""        # clear the input field
        # (no explicit st.rerun() needed inside callbacks)


def clear_completed_todos() -> None:
    """Erase the completed-todos file and refresh the app."""
    completed_list = functions.load_todos(FILEPATH_COMPLETED)
    functions.clear_completed(completed_list, FILEPATH_COMPLETED)
    # st.rerun()  # OK here because this function is called via st.button (on_click)


# -------- PAGE CONFIG ------------------------------------------------------
st.set_page_config(
    page_title="My Todo App",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------- CUSTOM CSS -------------------------------------------------------
st.markdown(
    """
    <style>
    .main-header        { text-align:center; color:#1f77b4; margin-bottom:2rem; }
    .subtitle           { text-align:center; color:#666;    margin-bottom:3rem; }

    .todo-container     { background-color:#ffffff; padding:1rem; border-radius:10px;
                          border:1px solid #e9ecef; margin-bottom:1rem; }
    .completed-container{ background-color:#ffffff; padding:1rem; border-radius:10px;
                          border:1px solid #c8e6c9; margin-bottom:1rem; }

    .stTextInput > div > div > input { border-radius:20px; }

    .stButton > button {
        border-radius:20px; border:none;
        background:linear-gradient(90deg,#1f77b4,#17a2b8); color:white;
    }
    .stButton > button:hover {
        background:linear-gradient(90deg,#17a2b8,#1f77b4);
        transform:translateY(-2px); transition:all .3s;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------- TITLE & SUBTITLE --------------------------------------------------
st.markdown('<h1 class="main-header">📋 My Todo App</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Stay organized and boost your productivity!</p>',
    unsafe_allow_html=True,
)

# -------- SESSION STATE INIT -----------------------------------------------
if "processed_indices" not in st.session_state:
    st.session_state.processed_indices = set()

# -------- READ DATA FROM DISK ----------------------------------------------
todo_list      = functions.load_todos(FILEPATH_TODO)
completed_list = functions.load_todos(FILEPATH_COMPLETED)

# -------- MAIN LAYOUT (two columns) ----------------------------------------
col1, col2 = st.columns(2)

# -- ACTIVE TASKS (left column) ---------------------------------------------
with col1:
    st.markdown('<div class="todo-container">', unsafe_allow_html=True)
    st.subheader("📝 Active Tasks")

    if not todo_list:
        st.info("🎉 No active tasks! Add one above to get started.")
    else:
        for idx, todo in enumerate(todo_list):
            # unique key prevents checkbox collisions if text repeats
            checkbox_key = f"todo_{idx}_{hash(todo)}"
            checked = st.checkbox(todo, key=checkbox_key, value=False)

            if checked:
                # move from active list to completed list
                functions.complete(idx, todo_list, completed_list)
                st.session_state.processed_indices.clear()
                st.rerun()  # immediate visual update after ticking the box
    st.markdown("</div>", unsafe_allow_html=True)

# -- COMPLETED TASKS (right column) -----------------------------------------
with col2:
    st.markdown('<div class="completed-container">', unsafe_allow_html=True)
    st.subheader("✅ Completed Tasks")

    if not completed_list:
        st.info("📋 No completed tasks yet. Check off some todos!")
    else:
        for comp in completed_list:
            st.markdown(f"~~{comp}~~ ✓")

    if completed_list:
        # button calls clear_completed_todos() which then st.rerun()s
        st.button("🗑️ Clear All Completed", key="clear_completed",
                  on_click=clear_completed_todos)
    st.markdown("</div>", unsafe_allow_html=True)

# -------- CENTERED INPUT FIELD ---------------------------------------------
left_spacer, center, right_spacer = st.columns([1, 2, 1])

with center:
    st.text_input(
        "",                        # empty label
        key="new_todo",
        on_change=add_todo,        # callback defined above
        placeholder="What needs to be done?",
        label_visibility="collapsed",
        help="Press Enter to add your todo",
    )

# -------- FOOTER METRICS ----------------------------------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📋 Active Tasks", len(todo_list))
with col2:
    st.metric("✅ Completed Tasks", len(completed_list))
with col3:
    st.metric("📊 Total Tasks", len(todo_list) + len(completed_list))

# Additional styling for the metric boxes
st.markdown(
    """
    <style>
    [data-testid="metric-container"] {
        background-color:#ffffff; border:1px solid #e0e0e0;
        padding:1rem; border-radius:10px;
        box-shadow:0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
