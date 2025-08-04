import functions
import os
import FreeSimpleGUI as sg
from datetime import datetime

# To rebuild your To-Do app executable with PyInstaller, you should use the following command:
# -> pyinstaller --onefile --windowed --clean gui.py
# Here's what each option means:
# --onefile (not --oneline): Packages your app as a single executable file, making distribution easier.
# --windowed: Ensures that no command line console window appears when your GUI app runs (recommended for GUI apps).
# --clean: Cleans the PyInstaller cache and removes temporary files before building (a good practice after changing source code, especially file paths).

# ============================
# File Paths for Data Persistence
# ============================

r"""
This code creates a hidden folder named .todo_app inside the current user's home directory
(e.g., C:\Users\Username on Windows or /home/username on Linux/macOS) to store application data files.
It ensures the folder exists using os.makedirs with exist_ok=True, which avoids errors if the folder is already present.
The two file paths defined within this folder (todo_list.txt and completed_todo_list.txt) are used to persist the user's to-do data
safely and reliably across program runs, regardless of where the program or executable is launched from.
"""

# Use the user's home directory with a .todo_app subfolder
APPDATA_DIR = os.path.join(os.path.expanduser("~"), ".todo_app")
os.makedirs(APPDATA_DIR, exist_ok=True)  # Ensure the directory exists

FILEPATH_TODO = os.path.join(APPDATA_DIR, "todo_list.txt")
FILEPATH_COMPLETED_TODO = os.path.join(APPDATA_DIR, "completed_todo_list.txt")

# Create file if it does not exist (empty)
if not os.path.isfile(FILEPATH_TODO):
    with open(FILEPATH_TODO, 'w', encoding='utf-8'):
        pass
if not os.path.isfile(FILEPATH_COMPLETED_TODO):
    with open(FILEPATH_COMPLETED_TODO, 'w', encoding='utf-8'):
        pass


# ============================
# Function to Create New Window Each Time (for Theme Switching)
# ============================


def create_window(current_theme='DarkGrey15'):
    """
    Set the global theme and create a new GUI window with fresh elements.
    This supports dynamic switching between themes by closing the old window
    and creating a new one with the selected theme applied.

    Args:
        current_theme (str): The theme name to apply before window creation.

    Returns:
        sg.Window: A new PySimpleGUI window instance.
    """
    sg.theme(current_theme)

    # GUI Elements Creation
    clock = sg.Text('', key='clock')
    label = sg.Text("Type in a To-Do: ", font=("helvetica", 11))
    dark_theme_button = sg.Button("Dark Theme", key="dark_theme")
    light_theme_button = sg.Button("Light Theme", key="light_theme")
    input_box = sg.InputText(tooltip="Enter To-Do", key='todo', font=("helvetica", 14))  # type: ignore
    add_button = sg.Button('Add', size=8, mouseover_colors=('white', 'black'))
    input_box_todo_list = sg.Text("Your To-Do List: ", font=("helvetica", 11))
    list_box = sg.Listbox(
        values=todo_list,
        key='todos',
        enable_events=True,
        size=[70, 9],
        font=("helvetica", 11)
    )
    edit_button = sg.Button('Edit', size=8, mouseover_colors=('white', 'black'))
    input_box_comp_todo_list = sg.Text("Your Completed To-Do List: ", font=("helvetica", 11))
    list_box_for_completed_todo = sg.Listbox(
        values=completed_todo_list,
        key='comp_todos',
        enable_events=True,
        size=[70, 9],
        font=("helvetica", 11)
    )
    complete_button = sg.Button('Complete', size=8, mouseover_colors=('white', 'black'))
    remove_button = sg.Button('Remove', size=8, mouseover_colors=('white', 'black'))
    clear_completed_todos = sg.Button('Clear Completed Todos', size=20, mouseover_colors=('white', 'black'))
    exit_button = sg.Button('Exit', size=8, mouseover_colors=('white', 'black'))

    # Layout arrangement, with sg.Push() to push buttons right in first row
    layout = [
        [clock, sg.Push(), dark_theme_button, light_theme_button],
        [label],
        [input_box],
        [add_button, remove_button],
        [input_box_todo_list],
        [list_box, edit_button],
        [input_box_comp_todo_list],
        [list_box_for_completed_todo],
        [complete_button, clear_completed_todos, sg.Push(), exit_button]
    ]

    # finalize=True lets GUI be fully created and elements accessible immediately
    # important so that updates can be made right after creating the window
    return sg.Window("My To-Do App", layout, font=("helvetica", 10), finalize=True)


# ============================
# Loading Existing Todos from Files into Lists
# ============================

# Reading todos: open files in 'a+' mode to read and create if missing
with open(FILEPATH_TODO, "a+", encoding="utf-8") as file:
    file.seek(0)  # Reset file pointer to start
    todo_list = [line.strip() for line in file if line.strip()]  # Strip whitespace, ignore empty lines

with open(FILEPATH_COMPLETED_TODO, "a+", encoding="utf-8") as file:
    file.seek(0)
    completed_todo_list = [line.strip() for line in file if line.strip()]

# ============================
# Initialize Theme Variable and Create First Window
# ============================

current_theme = 'DarkGrey15'  # Default starting theme, matches create_window default
window = create_window(current_theme)

# Copy lists for external change detection
last_todos = list(todo_list)
last_completed = list(completed_todo_list)

# Function references to reload todos externally
read_todos = functions.load_todos(filepath=FILEPATH_TODO)
read_comp_todos = functions.load_comp_todos(filepath2=FILEPATH_COMPLETED_TODO)

# ============================
# Main Event Loop
# ============================

while True:
    # window.read() with timeout to update clock periodically and remain responsive
    event, values = window.read(timeout=400)  # wait max 400ms for events # type: ignore

    # ---------- Theme Switching Logic ----------
    # When user clicks theme buttons:
    # 1. Update current_theme string
    # 2. Close old window
    # 3. Create new window with new theme via create_window()
    # 4. Update listboxes in new window to reflect current data lists
    if event == "dark_theme":
        current_theme = 'DarkGrey15'
        window.close()
        window = create_window(current_theme)
        try:
            window['todos'].update(values=todo_list)  # refresh todo list display # type: ignore
            window['comp_todos'].update(values=completed_todo_list)  # refresh completed todos display # type: ignore
        except Exception:
            # Timing issues with update right after recreation can cause exceptions
            # Silently ignore here for robustness
            pass

    elif event == "light_theme":
        current_theme = 'LightGrey2'
        window.close()
        window = create_window(current_theme)
        try:
            window['todos'].update(values=todo_list)  # type: ignore
            window['comp_todos'].update(values=completed_todo_list)  # type: ignore
        except Exception:
            pass

    # ---------- Exit Handling ----------
    if event in [sg.WIN_CLOSED, 'Exit']:
        break  # Exit the program cleanly

    # ---------- Clock Update ----------
    # Update clock Text element with current date/time every iteration
    current_time = datetime.now().strftime("Today's Date:%m/%d/%Y\nTime: %I:%M %p")
    window['clock'].update(value=current_time)  # type: ignore

    # ---------- Poll for external file changes ----------
    # Refresh todos from external file changes detected by functions.load_todos functions
    new_todos = read_todos
    new_completed = read_comp_todos

    # If new values differ, update GUI and in-memory variables
    if new_todos != last_todos:
        todo_list[:] = new_todos  # Update main list in-place
        window['todos'].update(values=todo_list)  # type: ignore
        last_todos = list(new_todos)

    if new_completed != last_completed:
        completed_todo_list[:] = new_completed
        window['comp_todos'].update(values=completed_todo_list)  # type: ignore
        last_completed = list(new_completed)

    # ---------- Debug prints (optional) ----------
    print("Event:", event)  # Log which event was triggered
    print("Values:", values)  # Log current input values for debugging

    # ---------- User Interaction Event Handling ----------
    # Use Python 3.10+ match statement to respond to events
    match event:

        case "Add":
            todo = values['todo'].strip()
            if todo:
                # Add the new todo item using the imported function
                functions.add(todo, todo_list)
                window['todos'].update(values=todo_list)  # Update listbox # type: ignore
                window['todo'].update(value='')  # Clear inputbox # type: ignore
            else:
                # Show error popup if input is empty
                sg.popup(
                    "You haven't written any todo to add.\nWrite a todo for adding.",
                    font=("helvetica", 10),
                    title="ERROR!!!"
                )

        case "Remove":
            try:
                todo_to_remove = values['todos'][0]  # get selected todo item
                index = todo_list.index(todo_to_remove)  # find index in list
                functions.remove(index, todo_list)  # remove todo
                window['todos'].update(values=todo_list)  # update display # type: ignore
                window['todo'].update(value='')  # clear input box # type: ignore
            except IndexError:
                sg.popup(
                    "You haven't selected any todo to remove.\nSelect a todo to remove.",
                    font=("helvetica", 10),
                    title="ERROR!!!"
                )

        case "Edit":
            try:
                todo_to_edit = values['todos'][0]  # selected todo item
                new_todo = values['todo']  # new text from input box
                index = todo_list.index(todo_to_edit)
                functions.edit(index, new_todo, todo_list, completed_todo_list)
                window['todos'].update(values=todo_list)  # update display # type: ignore
                window['todo'].update(value='')  # clear input box # type: ignore
            except IndexError:
                sg.popup(
                    "You haven't selected any todo to edit.\nSelect a todo to edit.",
                    font=("helvetica", 10),
                    title="ERROR!!!"
                )

        case "Complete":
            try:
                todo_to_complete = values['todos'][0]
                index = todo_list.index(todo_to_complete)
                functions.complete(index, todo_list, completed_todo_list)
                window['comp_todos'].update(values=completed_todo_list)  # update completed todos # type: ignore
                window['todos'].update(values=todo_list)  # update todo list # type: ignore
                window['todo'].update(value='')  # clear input box # type: ignore
            except IndexError:
                sg.popup(
                    "You haven't selected any todo for completion.\nSelect a todo for completing.",
                    font=("helvetica", 10),
                    title="ERROR!!!"
                )

        case "Clear Completed Todos":
            functions.clear_completed(completed_todo_list)
            window['comp_todos'].update(values=completed_todo_list)  # refresh display # type: ignore 

        case "todos":
            # When a todo item listbox selection changes,
            # extract the todo text without the date suffix and fill input box for editing
            try:
                selected_todo = values['todos'][0]
                # Remove the last 24 chars containing "(Created on: DD/MM/YYYY)"
                todo_without_date = selected_todo[:-24]
                window['todo'].update(value=todo_without_date)  # type: ignore
            except IndexError:
                sg.popup(
                    "First add a todo, then select from the list.",
                    font=("helvetica", 10),
                    title="ERROR!!!"
                )

        case "comp_todos":
            # Clear input box when completed todos are selected (optional UX)
            window['todo'].update(value="")  # type: ignore

# ============================
# Cleanup on Exit
# ============================

window.close()
