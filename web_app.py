import streamlit as st
import os
import functions

# Setup data folder
APPDATA_DIR = os.path.join(os.path.expanduser("~"), ".todo_app")
os.makedirs(APPDATA_DIR, exist_ok=True)

FILEPATH_TODO = os.path.join(APPDATA_DIR, "todo_list.txt")
FILEPATH_COMPLETED = os.path.join(APPDATA_DIR, "completed_todo_list.txt")

if not os.path.isfile(FILEPATH_TODO):
    open(FILEPATH_TODO, 'w').close()
if not os.path.isfile(FILEPATH_COMPLETED):
    open(FILEPATH_COMPLETED, 'w').close()

# Load todos lists
todo_list = functions.load_todos(FILEPATH_TODO)
completed_list = functions.load_todos(FILEPATH_COMPLETED)

def add_todo():
    todos = st.session_state["new_todo"].strip()
    if todos:
        functions.add(todos, todo_list)
        functions.save_todos(FILEPATH_TODO, todo_list)
        st.session_state["new_todo"] = ""

# Center aligned header
st.markdown("""
    <h1 style='text-align: center;'>📋 My Todo App</h1>
    <h4 style='text-align: center; color: gray;'>Use to increase your productivity.</h4>
""", unsafe_allow_html=True)

if "processed_indices" not in st.session_state:
    st.session_state.processed_indices = set()

st.text_input("",placeholder="Enter a todo...", key="new_todo", on_change=add_todo)

col1, col2 = st.columns(2)

with col1:
    st.header("📝 To-Do List")
    # Create a container with fixed height and scrollable content
    with st.container(height=300):
        for idx, todo in enumerate(todo_list):
            checked = st.checkbox(todo, key=f"todo_{idx}")
            if checked and idx not in st.session_state.processed_indices:
                # Process completion
                functions.complete(idx, todo_list, completed_list)
                functions.save_todos(FILEPATH_TODO, todo_list)
                functions.save_todos(FILEPATH_COMPLETED, completed_list)
                # Mark as processed
                st.session_state.processed_indices.add(idx)
                # Force rerun to update UI with new lists and reset checkboxes
                st.rerun()

with col2:
    st.header("✅ Completed Tasks")
    # Create a container with fixed height and scrollable content
    with st.container(height=300):
        for comp in completed_list:
            st.markdown(f"~~{comp}~~")

# Fix the clear completed function call
def clear_completed_todos():
    functions.clear_completed(completed_list, FILEPATH_COMPLETED)

st.button("Clear Completed Todos", on_click=clear_completed_todos)
