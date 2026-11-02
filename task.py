from datetime import datetime

from db import get_connection


VALID_PRIORITIES = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

VALID_STATUSES = [
    "Pending",
    "In Progress",
    "Completed",
    "On Hold"
]


def get_valid_priority():

    while True:

        print("\nSelect priority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Critical")

        choice = input("Enter your choice: ")

        priority_map = {
            "1": "Low",
            "2": "Medium",
            "3": "High",
            "4": "Critical"
        }

        if choice in priority_map:
            return priority_map[choice]

        print("Invalid priority. Please try again.")


def get_valid_date():

    while True:

        due_date = input(
            "Enter due date (YYYY-MM-DD): "
        ).strip()

        try:

            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

            return due_date

        except ValueError:

            print(
                "Invalid date format. "
                "Please use YYYY-MM-DD."
            )


def create_task():

    print("\n========== CREATE TASK ==========")

    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return

    description = input(
        "Enter task description: "
    ).strip()

    priority = get_valid_priority()

    due_date = get_valid_date()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO tasks
    (title, description, priority, due_date)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        title,
        description,
        priority,
        due_date
    )

    try:

        cursor.execute(query, values)
        conn.commit()

        print("\nTask created successfully!")

    except Exception as e:

        conn.rollback()

        print("\nCould not create task.")
        print("Error:", e)

    cursor.close()
    conn.close()


def view_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        title,
        description,
        priority,
        due_date,
        status,
        created_at
    FROM tasks
    ORDER BY id
    """

    cursor.execute(query)

    tasks = cursor.fetchall()

    if len(tasks) == 0:

        print("\nNo tasks found.")

    else:

        print("\n========== TASK LIST ==========")

        for task in tasks:

            print("\nTask ID:", task[0])
            print("Title:", task[1])
            print("Description:", task[2])
            print("Priority:", task[3])
            print("Due Date:", task[4])
            print("Status:", task[5])
            print("Created At:", task[6])

    cursor.close()
    conn.close()


def task_exists(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id
    FROM tasks
    WHERE id = %s
    """

    cursor.execute(
        query,
        (task_id,)
    )

    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return task is not None


def update_task():

    print("\n========== UPDATE TASK ==========")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():

        print("Task ID must be a number.")
        return

    task_id = int(task_id)

    if not task_exists(task_id):

        print("Task not found.")
        return

    title = input(
        "Enter new task title: "
    ).strip()

    if title == "":
        print("Task title cannot be empty.")
        return

    description = input(
        "Enter new task description: "
    ).strip()

    priority = get_valid_priority()

    due_date = get_valid_date()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tasks
    SET title = %s,
        description = %s,
        priority = %s,
        due_date = %s
    WHERE id = %s
    """

    values = (
        title,
        description,
        priority,
        due_date,
        task_id
    )

    try:

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            print("\nTask updated successfully!")
        else:
            print("\nNo changes were made.")

    except Exception as e:

        conn.rollback()

        print("\nCould not update task.")
        print("Error:", e)

    cursor.close()
    conn.close()


def delete_task():

    print("\n========== DELETE TASK ==========")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():

        print("Task ID must be a number.")
        return

    task_id = int(task_id)

    if not task_exists(task_id):

        print("Task not found.")
        return

    confirm = input(
        "Are you sure you want to delete this task? (y/n): "
    ).lower()

    if confirm != "y":

        print("Task deletion cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    DELETE FROM tasks
    WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (task_id,)
        )

        conn.commit()

        print("\nTask deleted successfully!")

    except Exception as e:

        conn.rollback()

        print("\nCould not delete task.")
        print("Error:", e)

    cursor.close()
    conn.close()


def update_task_status():

    print("\n========== UPDATE TASK STATUS ==========")

    task_id = input("Enter task ID: ").strip()

    if not task_id.isdigit():

        print("Task ID must be a number.")
        return

    task_id = int(task_id)

    if not task_exists(task_id):

        print("Task not found.")
        return

    print("\nSelect new status:")
    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")
    print("4. On Hold")

    choice = input("Enter your choice: ")

    status_map = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed",
        "4": "On Hold"
    }

    if choice not in status_map:

        print("Invalid status choice.")
        return

    new_status = status_map[choice]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tasks
    SET status = %s
    WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (
                new_status,
                task_id
            )
        )

        conn.commit()

        if cursor.rowcount > 0:
            print(
                "\nTask status updated successfully!"
            )
        else:
            print("No changes were made.")

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not update task status."
        )
        print("Error:", e)

    cursor.close()
    conn.close()


def task_menu():

    while True:

        print("\n========== TASK MANAGEMENT ==========")
        print("1. Create Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Update Task Status")
        print("6. Back")

        choice = input(
            "Enter your choice: "
        )

        if choice == "1":

            create_task()

        elif choice == "2":

            view_tasks()

        elif choice == "3":

            update_task()

        elif choice == "4":

            delete_task()

        elif choice == "5":

            update_task_status()

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )