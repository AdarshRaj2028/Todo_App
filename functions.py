import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILEPATH_TODO = os.path.join(BASE_DIR, "todo_list.txt")
FILEPATH_COMPLETED_TODO = os.path.join(BASE_DIR, "completed_todo_list.txt")

# =========================
# Todo App Functions
# =========================

MAX_TODO_LENGTH = 200  # or any limit you prefer


def add(user_input: str, todo_list: list, filepath=FILEPATH_TODO) -> None:
    """
    Add a new todo item to the todo_list after validating and normalizing the input.
    - Strips whitespace, collapses multiple spaces, capitalizes each word, and ensures punctuation.
    - Ignores empty input.
    """
    user_input = user_input.title().strip()
    user_input = " ".join(user_input.split())  # Removes in between extra spaces

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
    todo_with_date = f"{user_input}(Created on: {current_date})"

    # Add to the passed list instead of the main.todo_list
    todo_list.append(todo_with_date)

    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(todo_with_date + "\n")


def remove(index: int, todo_list: list, filepath=FILEPATH_TODO):
    """Remove todo at specified index and update file."""
    todo_list.pop(index)

    # Update remaining todos in file
    with open(filepath, 'w', encoding='utf-8') as f:
        for todos in todo_list:
            f.write(f"{todos}\n")

    print("\n***✅ Todo removed successfully!***")
    show_todo_list(todo_list)


def show(todo_list: list, completed_todo_list: list) -> None:
    """
    Display all current todos and completed todos.
    - Todos are shown in the order they were added.
    - Completed todos are shown with a '---> Done' marker.
    """
    print("\n" + "="*81)

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

    print("="*81)


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

    # Check if the new todo is not blank or only whitespaces
    if not new_todo:
        print("⚠️ You have not entered any Todo. Please enter a Todo.")
        pause_terminal()
        clear_terminal()
        return

    # Add punctuation at the end if not present
    if not new_todo.endswith((".", "?", "!")):
        new_todo += "."

    current_date = time.strftime("%d/%m/%Y")
    new_todo_with_date = f"{new_todo}(Created on: {current_date})"

    # Update todo in memory list
    todo_list[index] = new_todo_with_date

    # Update todos in the file
    with open(filepath, 'w', encoding='utf-8') as f:
        for todos in todo_list:
            f.write(f"{todos}\n")

    print("\n***✅ Todo updated successfully!***")
    print("\n📝 Your New Todo List:\n")

    for i, items in enumerate(todo_list, 1):
        print(f"{i}. {items}")

    if not completed_todo_list:
        print("\n✅ Your Completed Todo List:\n\n-> You have not completed any Todo Task.")
    else:
        show_completed_todo()


def complete(index: int, todo_list: list, completed_todo_list: list, filepath=FILEPATH_COMPLETED_TODO, filepath2=FILEPATH_TODO) -> None:
    """
    Mark a todo as completed by moving it from todo_list to completed_todo_list.
    - Index is 1-based from user input, converted 0-based.
    """
    # Use pop to remove and reuse the string for completed tasks
    poped_todo = todo_list.pop(index)

    # Add to completed todos file
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(poped_todo + "\n")

    completed_todo_list.append(poped_todo)

    # Update remaining todos in file
    with open(filepath2, 'w', encoding='utf-8') as f:
        for todos in todo_list:
            f.write(f"{todos}\n")

    print("\n🎉 Todo marked as completed!")
    show_completed_todo()


def show_completed_todo(filepath=FILEPATH_COMPLETED_TODO) -> None:
    """Display all completed todos with completion markers."""
    print("\n✅ Your Completed Todo List:\n")

    # Read directly from file to display completed tasks
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, todos in enumerate(f, 1):
            print(f"{i}. {todos.strip()} ---> Done")


def clear_completed(completed_todo_list: list, filepath=FILEPATH_COMPLETED_TODO) -> None:
    """
    Clear all completed todos from memory and file.
    So that completed_todo_list file doesn't get overfilled after many usage
    (although, which would have taken years to fill)
    """
    # Clear completed todos from memory and reset list
    completed_todo_list.clear()

    # Method 1
    # open("completed_todo_list.txt", "w", encoding="utf-8").close()

    # Method 2 (Preferable)
    with open(filepath, "w", encoding="utf-8"):
        pass

    print("✅ All completed todos have been cleared.")


def prompt_for_todo_selection(todo_list: list) -> None | int:
    """Prompt user to select a todo and return its index, or None if invalid."""
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
            return index_for_todo - 1  # Returns the 0 based index
        else:
            print("\n⚠️ The value is out of range of the number of todos you have.")
            return None

    except ValueError as e:
        print(f"\n⚠️ You have entered a string(Todo) instead of an integer(Todo Number).\nError: {e}")
        pause_terminal()
        clear_terminal()
        return None

    except IndexError as I:
        print(f"\n⚠️ Index Entered is out of range.\nError: {I}")
        pause_terminal()
        clear_terminal()
        return None


def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause_terminal() -> None:
    """Pause the terminal screen."""
    input("\nPress Enter to continue...")
