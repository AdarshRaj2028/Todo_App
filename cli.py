import datetime
import functions

FILEPATH_TODO = "Todo_App_Project_1/main/todo_list.txt"
FILEPATH_COMPLETED_TODO = "Todo_App_Project_1/main/completed_todo_list.txt"
# =========================
#   Main Program Loop
# =========================

'''
IMPORTANT INFO TO REMEMBER:
In memory(RAM): your todos are a Python list of strings.
On disk(Storage): your todos are stored as plain text, one string per line.
You convert between these using file reading/writing in your code.
'''
def main(filepath=FILEPATH_TODO, filepath2=FILEPATH_COMPLETED_TODO):
    """
    Main loop: handles user input and calls the appropriate functions.
    """
    todo_list = []
    completed_todo_list = []
    
    # Ensure files exist - create if they don't, do nothing if they do
    # Using 'a' mode only creates if file doesn't exist, won't overwrite existing content
    with open(filepath, "a", encoding="utf-8") as f:
        pass
    
    with open(filepath2, "a", encoding="utf-8") as f:
        pass

    # Load existing todos from files into Python lists at program startup
    # These lines are essential for converting file contents into Python lists
    # Without them, lists would not be populated and app wouldn't remember previous todos
    
    # Read all non-empty lines from todo file and create list
    # line.strip() ensures only non-empty, meaningful lines are added
    with open(filepath, 'r', encoding='utf-8') as f:  
        todo_list = [line.strip() for line in f if line.strip()]
    
    # Create list of all non-empty, trimmed completed todos from file
    # Could also use readlines() but list comprehension is more pythonic
    # readlines() is more general-purpose but less concise than list comprehension
    with open(filepath2, 'r', encoding='utf-8') as f:
        completed_todo_list = [line.strip() for line in f if line.strip()]

    # Define command aliases for better organization and maintainability
    ADD_COMMANDS: list[str] = ["add", "1"]
    REMOVE_COMMANDS: list[str] = ["remove", "2"]
    SHOW_COMMANDS: list[str] = ["show", "display", "3"]
    EDIT_COMMANDS: list[str] = ["edit", "4"]
    COMPLETE_COMMANDS: list[str] = ["complete", "5"]
    CLEAR_COMMANDS: list[str] = ["clear", "6"]
    EXIT_COMMANDS: list[str] = ["exit", "7"]
    MENU_TEXT: str = """
📝 TODO APP COMMANDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ADD:      'add' or '1'           | Quick: 'add buy milk'
  REMOVE:   'remove' or '2'        | Quick: 'remove <number>'
  SHOW:     'show' or '3'          | Also: 'display'
  EDIT:     'edit' or '4'          | Quick: 'edit <number>'
  COMPLETE: 'complete' or '5'      | Quick: 'complete <number>'
  CLEAR:    'clear' or '6'         | Clears completed tasks
  EXIT:     'exit' or '7'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter command: """
    
    while True:
        print("\n" + "="*81)
        user_action: str = input(MENU_TEXT).strip().lower()
        print("=" * 81)

        # Check for empty input
        if not user_action:
            print("⚠️  Please enter a valid option.\n")
            functions.pause_terminal()
            functions.clear_terminal()
            continue

        # Handle "add <todo_text>" format - user can type todo directly
        if user_action.startswith("add") and len(user_action) > 4:
            todo_item = user_action[4:]
            functions.add(todo_item, todo_list)
            print("\n✅ Your Todo Task Has Been Added Successfully!")
            functions.pause_terminal()
            functions.clear_terminal()

        # Handle regular add command
        elif user_action in ADD_COMMANDS:
            user_input: str = input("Enter your Todo: ")
            functions.add(user_input, todo_list)
            print("\n✅ Your Todo Task Has Been Added Successfully!")
            functions.pause_terminal()
            functions.clear_terminal()

        elif user_action in REMOVE_COMMANDS:
            selected_todo_to_remove = functions.prompt_for_todo_selection(todo_list)
            if selected_todo_to_remove is not None:
                functions.remove(selected_todo_to_remove, todo_list)  
                functions.pause_terminal()
                functions.clear_terminal()

        elif user_action.startswith("remove") and len(user_action) > 7:
            if not todo_list:
                print("\n⚠️  Your Todo list is empty. Please add a Todo first.")
                functions.pause_terminal()
                functions.clear_terminal()
                continue
            try:
                remove_todo_index = int(user_action[7:])
                if 0 < remove_todo_index <= len(todo_list):  # Check the original number
                    functions.remove(remove_todo_index - 1, todo_list) # Then convert to 0-based
                    functions.pause_terminal()
                    functions.clear_terminal()
                else:
                    print("\n⚠️  The value is out of range of the number of todos you have.")
                    functions.pause_terminal()
                    functions.clear_terminal()
                    continue
            except ValueError as e:
                print(f"\n⚠️  You have entered a string(todo) instead of an integer(todo number).\nError: {e}")
                functions.pause_terminal()
                functions.clear_terminal()
                continue


        # Handle show/display command
        elif user_action in SHOW_COMMANDS:
            functions.show(todo_list, completed_todo_list)
            functions.pause_terminal()
            functions.clear_terminal()

        # Handle edit command
        elif user_action in EDIT_COMMANDS:
            selected_todo = functions.prompt_for_todo_selection(todo_list)
            if selected_todo is not None:
                new_todo = input("Enter your new todo: ")
                functions.edit(selected_todo, new_todo, todo_list, completed_todo_list)
                functions.pause_terminal()
                functions.clear_terminal()    

        # Handle "edit <todo_number>" format - user can edit todo directly
        elif user_action.startswith("edit") and len(user_action) > 5:
            if not todo_list:
                print("\n⚠️  Your Todo list is empty. Please add a Todo first.")
                functions.pause_terminal()
                functions.clear_terminal()
                continue
            try:
                new_todo_item = int(user_action[5:])
                if 0 < new_todo_item <= len(todo_list):  # Check the original number
                    new_todo = input("Enter your new todo: ")
                    functions.edit(new_todo_item - 1, new_todo, todo_list, completed_todo_list) # Then convert to 0-based
                    functions.pause_terminal()
                    functions.clear_terminal()
                else:
                    print("\n⚠️  The value is out of range of the number of todos you have.")
                    functions.pause_terminal()
                    functions.clear_terminal()
                    continue
            except ValueError as e:
                print(f"\n⚠️  You have entered a string(todo) instead of an integer(todo number).\nError: {e}")
                functions.pause_terminal()
                functions.clear_terminal()
                continue

        # Handle complete command
        elif user_action in COMPLETE_COMMANDS:
            
            selected_todo = functions.prompt_for_todo_selection(todo_list)
            if selected_todo is not None:
                functions.complete(selected_todo, todo_list, completed_todo_list)
                functions.pause_terminal()
                functions.clear_terminal()
        
	# Handle "complete <todo_number>" format - user can complete todo directly
        elif user_action.startswith("complete") and len(user_action) > 8:
            if not todo_list:
                print("\n⚠️  Your Todo list is empty. Please add a Todo first.")
                functions.pause_terminal()
                functions.clear_terminal()
                continue
            try:
                new_todo_item = int(user_action[8:].strip())
                if 0 < new_todo_item <= len(todo_list):  # Check the original number
                    functions.complete(new_todo_item - 1, todo_list, completed_todo_list)  # Then convert to 0-based
                    functions.pause_terminal()
                    functions.clear_terminal()
                else:
                    print("\n⚠️  The value is out of range of the number of todos you have.")
                    functions.pause_terminal()
                    functions.clear_terminal()
                    continue
            except ValueError as e:
                print(f"\n⚠️  You have entered a string(Todo) instead of an integer(Todo number).\nError: {e}")
                functions.pause_terminal()
                functions.clear_terminal()
                continue

        # Handle clear completed command
        elif user_action in CLEAR_COMMANDS:
            functions.clear_completed(completed_todo_list)
            functions.pause_terminal()
            functions.clear_terminal()

        # Handle exit command
        elif user_action in EXIT_COMMANDS:
            print("\n***Thank you for using the Todo App!***\n")
            break

        # Handle invalid commands
        else:
            print("\n⚠️  Please enter a valid option.")
            functions.pause_terminal()
            functions.clear_terminal()

# =========================
#   Entry Point
# =========================
if __name__ == "__main__":
    current_datetime = datetime.datetime.now()
    current_time_str = current_datetime.strftime("Date: %A, %B %d, %Y | Time: %H:%M |")
    print("=" * 84)
    print(f"Welcome to the Todo Program | Today's {current_time_str}") 
    print("=" * 84)
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n***Exiting Todo Program. Goodbye!***")
    except EOFError:
        print("\n\nDetected end of input (EOF).\n***Exiting Todo Program. Goodbye!***")
    except UnicodeDecodeError as e:
        print(f"The files are being edited with a non-UTF-8 editor\bError: {e}")
        functions.pause_terminal()
        functions.clear_terminal()
    except Exception as e:
        print(f"An error occurred: {e}")
        functions.pause_terminal()
        functions.clear_terminal()
