import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("==============================")
print("       DEADLINE RESCUE")
print("==============================")

tasks = []

# Load saved tasks
try:
    with open("tasks.txt", "r") as file:
        saved_tasks = file.readlines()

    for line in saved_tasks:
        parts = line.strip().split(" | ")

        if len(parts) >= 3:
            task_name = parts[0]
            days = int(parts[1].replace(" days", ""))
            priority = parts[2]

            if len(parts) >= 4:
                status = parts[3]
            else:
                status = "Pending"

            tasks.append([task_name, days, priority, status])

except FileNotFoundError:
    print("No saved tasks found yet.")


# Calculate priority
def calculate_priority(days):
    if days <= 1:
        return "URGENT!"
    elif days <= 3:
        return "SOON"
    elif days <= 7:
        return "PLAN IT"
    else:
        return "LATER"


# Save all tasks
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(
                task[0] + " | " +
                str(task[1]) + " days | " +
                task[2] + " | " +
                task[3] + "\n"
            )


# Display tasks with deadline alerts
def show_tasks(status_filter="All"):
    found = False

    print("\nYOUR", status_filter.upper(), "TASKS")
    print("==============================")

    for i, task in enumerate(tasks):
        if status_filter == "All" or task[3] == status_filter:
            found = True

            print("\nTask number:", i + 1)
            print("Task:", task[0])
            print("Days left:", task[1])

            if task[3] == "Completed":
                print("Deadline alert: TASK COMPLETED!")
            elif task[1] < 0:
                print("Deadline alert: OVERDUE!")
            elif task[1] == 0:
                print("Deadline alert: DUE TODAY!")
            elif task[1] == 1:
                print("Deadline alert: DUE TOMORROW!")
            else:
                print("Deadline alert: UPCOMING")

            print("Priority:", task[2])
            print("Status:", task[3])
            print("------------------------------")

    if found == False:
        print("No", status_filter.lower(), "tasks found.")


# Search for a task
def search_tasks():
    search_name = input("Enter the task name to search: ")
    found = False

    print("\nSEARCH RESULTS")
    print("==============================")

    for i, task in enumerate(tasks):
        if search_name.lower() in task[0].lower():
            found = True
            print("\nTask number:", i + 1)
            print("Task:", task[0])
            print("Days left:", task[1])
            print("Priority:", task[2])
            print("Status:", task[3])
            print("------------------------------")

    if found == False:
        print("No matching task found.")


# Edit a task
def edit_task():
    if len(tasks) == 0:
        print("No tasks available to edit.")
        return

    show_tasks("All")

    try:
        number = int(input("Enter the task number to edit: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number!")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    task = tasks[number - 1]

    print("\nLeave a field blank to keep its current value.")

    new_name = input("Enter new task name (" + task[0] + "): ")

    if new_name.strip() != "":
        task[0] = new_name.strip()

    new_days = input("Enter new days left (" + str(task[1]) + "): ")

    if new_days.strip() != "":
        try:
            days = int(new_days)

            if days < 0:
                print("Days cannot be negative!")
                return

            task[1] = days
            task[2] = calculate_priority(days)

        except ValueError:
            print("Please enter a whole number.")
            return

    save_tasks()
    print("Task updated and saved successfully!")


# Delete a task
def delete_task():
    if len(tasks) == 0:
        print("No tasks available to delete.")
        return

    show_tasks("All")

    try:
        number = int(input("Enter the task number to delete: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number!")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    task_name = tasks[number - 1][0]
    print("\nTask selected:", task_name)

    confirm = input("Are you sure you want to delete it? (Y/N): ")

    if confirm.lower() == "y":
        tasks.pop(number - 1)
        save_tasks()
        print("Task deleted successfully!")
    elif confirm.lower() == "n":
        print("Deletion cancelled. Your task is safe.")
    else:
        print("Invalid choice. Deletion cancelled.")


# Task statistics
def show_statistics():
    total = len(tasks)
    pending = 0
    completed = 0
    urgent = 0

    for task in tasks:
        if task[3] == "Pending":
            pending = pending + 1
        elif task[3] == "Completed":
            completed = completed + 1

        if task[2] == "URGENT!":
            urgent = urgent + 1

    print("\n===== TASK STATISTICS =====")
    print("Total tasks:", total)
    print("Pending tasks:", pending)
    print("Completed tasks:", completed)
    print("Urgent tasks:", urgent)
    print("===========================")


# Main menu
while True:
    print("\nMAIN MENU")
    print("1. View all tasks")
    print("2. Add a new task")
    print("3. Mark a task as completed")
    print("4. View pending tasks")
    print("5. View completed tasks")
    print("6. Search for a task")
    print("7. Edit a task")
    print("8. Delete a task")
    print("9. View task statistics")
    print("10. Exit")

    choice = input("Enter your choice (1-10): ")

    # Option 1: View all tasks
    if choice == "1":
        show_tasks("All")

    # Option 2: Add a new task
    elif choice == "2":
        task_name = input("Enter task name: ")

        if task_name.strip() == "":
            print("Task name cannot be empty!")
            continue

        try:
            days = int(input("How many days are left? "))

            if days < 0:
                print("Days cannot be negative!")
                continue

        except ValueError:
            print("Please enter a whole number.")
            continue

        priority = calculate_priority(days)
        tasks.append([task_name.strip(), days, priority, "Pending"])
        save_tasks()

        print("Task saved successfully!")

    # Option 3: Mark a task as completed
    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks available.")
            continue

        show_tasks("All")

        try:
            number = int(input("Enter the task number to complete: "))

            if number < 1 or number > len(tasks):
                print("Invalid task number!")
                continue

        except ValueError:
            print("Please enter a valid number.")
            continue

        if tasks[number - 1][3] == "Completed":
            print("This task is already completed.")
        else:
            tasks[number - 1][3] = "Completed"
            save_tasks()
            print("Task marked as completed!")

    # Option 4: View pending tasks
    elif choice == "4":
        show_tasks("Pending")

    # Option 5: View completed tasks
    elif choice == "5":
        show_tasks("Completed")

    # Option 6: Search for a task
    elif choice == "6":
        search_tasks()

    # Option 7: Edit a task
    elif choice == "7":
        edit_task()

    # Option 8: Delete a task
    elif choice == "8":
        delete_task()

    # Option 9: View task statistics
    elif choice == "9":
        show_statistics()

    # Option 10: Exit
    elif choice == "10":
        print("Thank you for using Deadline Rescue!")
        break

    else:
        print("Invalid choice! Please enter a number from 1 to 10.")
