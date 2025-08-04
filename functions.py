import os
import time

r"""
Below code creates a hidden folder named .todo_app inside the current user's home directory
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

# =========================
# Todo App Functions
# =========================

MAX_TODO_LENGTH = 200  # Maximum length allowed for a todo item


def load_todos(filepath): # This can be used to load both todo list and completed todo list
    """Load todo items from a file, ignoring empty lines."""
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def save_todos(filepath, todo_list):
    """Save the list of todos to a file."""
    with open(filepath, "w", encoding="utf-8") as file:
        for todo in todo_list:
            file.write(todo + '\n')

def save_comp_todos(filepath2, completed_todo_list):
    """Save the list of completed todos to a file."""
    with open(filepath2, "w", encoding="utf-8") as file:
        for todo in completed_todo_list:
            file.write(todo + '\n')


def add(user_input: str, todo_list: list, filepath=FILEPATH_TODO) -> None:
    """
    Add a new todo item to todo_list after validating and normalizing the input.

    - Strips whitespace, collapses multiple spaces, capitalizes each word, and ensures punctuation.
    - Ignores empty input.
    """
    user_input = user_input.title().strip()
    user_input = " ".join(user_input.split())  # Remove extra spaces between words

    if not user_input.endswith((".", "?", "!")):
        user_input += "."

    # Check if input is empty after processing (was only whitespace)
    if not user_input:
        print("⚠️ You have not entered any Todo. Please enter one.")
        pause_terminal()
        clear_terminal()
        return

    # Validate todo length doesn't exceed maximum allowed characters
    if len(user_input) > MAX_TODO_LENGTH:
        print(f"⚠️ Todo is too long! Please keep it under {MAX_TODO_LENGTH} characters.")
        pause_terminal()
        clear_terminal()
        return

    current_date = time.strftime("%d/%m/%Y")
    todo_with_date = f"{user_input} (Created on: {current_date})"

    # Add to the passed list
    todo_list.append(todo_with_date)
    save_todos(filepath, todo_list)

    print("\n***✅ Todo added successfully!***")
    show_todo_list(todo_list)


def remove(index: int, todo_list: list, filepath=FILEPATH_TODO) -> None:
    """Remove todo at specified index and update the file."""
    todo_list.pop(index)

    # Update remaining todos in the file
    with open(filepath, 'w', encoding='utf-8') as f:
        for todos in todo_list:
            f.write(f"{todos}\n")

    print("\n***✅ Todo removed successfully!***")
    show_todo_list(todo_list)


def show(todo_list: list, completed_todo_list: list) -> None:
    """
    Display all current todos and completed todos.

    - Todos are shown in the order they were added.
    - Completed todos are shown with a '--> Done' marker.
    """
    print("\n" + "=" * 81)

    # Show current todos
    if not todo_list:  # Check for empty todo list
        print("📝 Your Todo List:\n\n-> Your Todo list is empty. Add a Todo now and get back to work!")
    else:
        show_todo_list(todo_list)

    # Show completed todos
    if not completed_todo_list:  # Check if completed list is empty
        print("\n✅ Your Completed Todo List:\n\n-> You have not completed any Todo Task.")
    else:
        show_completed_todo()

    print("=" * 81)


def show_todo_list(todo_list, filepath=FILEPATH_TODO) -> None:
    """Display the current todo list."""
    if not todo_list:
        print("\n📝 Your Todo List:\n\n-> Your Todo list is empty. Add a Todo now and get back to work!")
    else:
        print("\n📝 Your Todo List:\n")
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, todos in enumerate(f, 1):
                print(f"{i}. {todos.strip()}")


def edit(index: int, new_todo: str, todo_list: list, completed_todo_list: list, filepath=FILEPATH_TODO) -> None:
    """
    Edit an existing todo item at the given index (0-based).
    
    - Normalizes the new todo text.
    - Updates the todo in place.
    """
    new_todo = new_todo.strip().title()
    new_todo = " ".join(new_todo.split())

    # Validate todo length doesn't exceed maximum allowed characters
    if len(new_todo.strip()) > MAX_TODO_LENGTH:
        print(f"⚠️ Todo is too long! Please keep it under {MAX_TODO_LENGTH} characters.")
        pause_terminal()
        clear_terminal()
        return

    # Check if the new todo is not blank or only whitespace
    if not new_todo:
        print("⚠️ You have not entered any Todo. Please enter a Todo.")
        pause_terminal()
        clear_terminal()
        return

    # Add punctuation at the end if not present
    if not new_todo.endswith((".", "?", "!")):
        new_todo += "."

    current_date = time.strftime("%d/%m/%Y")
    new_todo_with_date = f"{new_todo} (Created on: {current_date})"

    # Update todo in memory list
    todo_list[index] = new_todo_with_date

    # Update todos in the file
    save_todos(filepath, todo_list)

    print("\n***✅ Todo updated successfully!***")
    print("\n📝 Your New Todo List:\n")

    for i, items in enumerate(todo_list, 1):
        print(f"{i}. {items}")

    if not completed_todo_list:
        print("\n✅ Your Completed Todo List:\n\n-> You have not completed any Todo Task.")
    else:
        show_completed_todo()


def complete(index: int, todo_list: list, completed_todo_list: list, filepath2=FILEPATH_COMPLETED_TODO) -> None:
    """
    Mark a todo as completed by moving it from todo_list to completed_todo_list.
    
    Args:
        index (int): 0-based index of todo item in todo_list.
    """
    # Remove item from todo_list
    popped_todo = todo_list.pop(index)

    # Add to completed todos file (append mode)
    with open(filepath2, 'a', encoding='utf-8') as f:
        f.write(popped_todo + "\n")

    completed_todo_list.append(popped_todo)

    # Update todos file to save remaining todos
    save_todos(FILEPATH_TODO, todo_list)

    print("\n🎉 Todo marked as completed!")
    show_completed_todo()


def show_completed_todo(filepath2=FILEPATH_COMPLETED_TODO) -> None:
    """Display all completed todos with completion markers."""
    print("\n✅ Your Completed Todo List:\n")
    # Read directly from file to display completed tasks
    with open(filepath2, 'r', encoding='utf-8') as f:
        for i, todos in enumerate(f, 1):
            print(f"{i}. {todos.strip()} --> Done")


def clear_completed(completed_todo_list: list, filepath2=FILEPATH_COMPLETED_TODO) -> None:
    """
    Clear all completed todos from memory and file.
    Keeps the completed_todo_list file from getting overfilled after long-term usage.
    """
    # Clear the in-memory list
    completed_todo_list.clear()

    # Clear the file contents (Method 2 preferred)
    with open(filepath2, "w", encoding="utf-8"):
        pass

    print("✅ All completed todos have been cleared.")


def prompt_for_todo_selection(todo_list: list) -> None | int:
    """
    Prompt user to select a todo item.

    Returns 0-based index of selected todo or None if invalid.
    """
    if not todo_list:
        print("\n⚠️ Your Todo list is empty. Please add a Todo first.")
        pause_terminal()
        clear_terminal()
        return None

    show_todo_list(todo_list)

    try:
        prompt_text = "\nEnter the number of the Todo: "
        index_for_todo = int(input(prompt_text))
        if 0 < index_for_todo <= len(todo_list):
            return index_for_todo - 1  # 0-based index
        else:
            print("\n⚠️ The value is out of range of the number of todos you have.")
            return None
    except ValueError as e:
        print(f"\n⚠️ You have entered an invalid value. Please enter an integer.\nError: {e}")
        pause_terminal()
        clear_terminal()
        return None
    except IndexError as I:
        print(f"\n⚠️ Index entered is out of range.\nError: {I}")
        pause_terminal()
        clear_terminal()
        return None


def clear_terminal() -> None:
    """Clear the terminal screen (Windows and Unix compatible)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause_terminal() -> None:
    """Pause the terminal screen and wait for user input."""
    input("\nPress Enter to continue...")
