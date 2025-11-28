# todo.py
# Simple Console-based To-Do List Application

import os

FILENAME = "tasks.txt"


def load_tasks():
    """Load tasks from the file into a list."""
    tasks = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            tasks = [line.strip() for line in file.readlines()]
    return tasks


def save_tasks(tasks):
    """Save tasks to the file."""
    with open(FILENAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")


def add_task(tasks):
    """Add a new task."""
    task = input("Enter the task: ").strip()
    if task:
        tasks.append(task)
        save_tasks(tasks)
        print(f"✅ Task added: {task}")
    else:
        print("⚠️ Task cannot be empty!")


def view_tasks(tasks):
    """View all tasks."""
    if not tasks:
        print("📭 No tasks found.")
    else:
        print("\n📋 Your To-Do List:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")


def remove_task(tasks):
    """Remove a task by number."""
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter the task number to remove: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f"🗑️ Task removed: {removed}")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")


def main():
    tasks = load_tasks()
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            print("👋 Exiting... Your tasks are saved.")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
