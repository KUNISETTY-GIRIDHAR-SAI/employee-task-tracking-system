from db import get_connection

from dashboard import employee_dashboard_summary

from comments import (
    add_comment,
    view_comments
)


def show_my_tasks(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        tasks.id,
        tasks.title,
        tasks.description,
        tasks.priority,
        tasks.due_date,
        tasks.status,
        assigned_tasks.assigned_at
    FROM assigned_tasks

    JOIN tasks
        ON assigned_tasks.task_id = tasks.id

    WHERE assigned_tasks.employee_id = %s

    ORDER BY tasks.due_date
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    tasks = cursor.fetchall()

    if len(tasks) == 0:

        print(
            "\nNo tasks assigned to you."
        )

    else:

        print(
            "\n========== MY TASKS =========="
        )

        for task in tasks:

            print("\nTask ID:", task[0])
            print("Title:", task[1])
            print("Description:", task[2])
            print("Priority:", task[3])
            print("Due Date:", task[4])
            print("Status:", task[5])
            print("Assigned At:", task[6])

    cursor.close()
    conn.close()


def view_task_details(employee_id):

    print(
        "\n========== TASK DETAILS =========="
    )

    task_id = input(
        "Enter task ID: "
    ).strip()

    if not task_id.isdigit():

        print(
            "Task ID must be a number."
        )

        return

    task_id = int(task_id)

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        tasks.id,
        tasks.title,
        tasks.description,
        tasks.priority,
        tasks.due_date,
        tasks.status,
        assigned_tasks.assigned_at
    FROM assigned_tasks

    JOIN tasks
        ON assigned_tasks.task_id = tasks.id

    WHERE assigned_tasks.employee_id = %s
      AND tasks.id = %s
    """

    cursor.execute(
        query,
        (
            employee_id,
            task_id
        )
    )

    task = cursor.fetchone()

    if task is None:

        print(
            "\nTask not found or this task is not assigned to you."
        )

    else:

        print(
            "\n========== TASK DETAILS =========="
        )

        print(
            "Task ID:",
            task[0]
        )

        print(
            "Title:",
            task[1]
        )

        print(
            "Description:",
            task[2]
        )

        print(
            "Priority:",
            task[3]
        )

        print(
            "Due Date:",
            task[4]
        )

        print(
            "Status:",
            task[5]
        )

        print(
            "Assigned At:",
            task[6]
        )

    cursor.close()
    conn.close()


def filter_tasks(employee_id):

    print(
        "\n========== FILTER MY TASKS =========="
    )

    print("1. Filter by Status")
    print("2. Filter by Priority")
    print("3. Back")

    choice = input(
        "Enter your choice: "
    ).strip()

    conn = get_connection()
    cursor = conn.cursor()

    if choice == "1":

        print("\n1. Pending")
        print("2. In Progress")
        print("3. Completed")
        print("4. On Hold")

        status_choice = input(
            "Enter status choice: "
        ).strip()

        status_map = {
            "1": "Pending",
            "2": "In Progress",
            "3": "Completed",
            "4": "On Hold"
        }

        if status_choice not in status_map:

            print(
                "Invalid status choice."
            )

            cursor.close()
            conn.close()

            return

        status = status_map[
            status_choice
        ]

        query = """
        SELECT
            tasks.id,
            tasks.title,
            tasks.priority,
            tasks.due_date,
            tasks.status
        FROM assigned_tasks

        JOIN tasks
            ON assigned_tasks.task_id = tasks.id

        WHERE assigned_tasks.employee_id = %s
          AND tasks.status = %s

        ORDER BY tasks.due_date
        """

        cursor.execute(
            query,
            (
                employee_id,
                status
            )
        )

    elif choice == "2":

        print("\n1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Critical")

        priority_choice = input(
            "Enter priority choice: "
        ).strip()

        priority_map = {
            "1": "Low",
            "2": "Medium",
            "3": "High",
            "4": "Critical"
        }

        if priority_choice not in priority_map:

            print(
                "Invalid priority choice."
            )

            cursor.close()
            conn.close()

            return

        priority = priority_map[
            priority_choice
        ]

        query = """
        SELECT
            tasks.id,
            tasks.title,
            tasks.priority,
            tasks.due_date,
            tasks.status
        FROM assigned_tasks

        JOIN tasks
            ON assigned_tasks.task_id = tasks.id

        WHERE assigned_tasks.employee_id = %s
          AND tasks.priority = %s

        ORDER BY tasks.due_date
        """

        cursor.execute(
            query,
            (
                employee_id,
                priority
            )
        )

    elif choice == "3":

        cursor.close()
        conn.close()

        return

    else:

        print(
            "Invalid choice."
        )

        cursor.close()
        conn.close()

        return

    tasks = cursor.fetchall()

    if len(tasks) == 0:

        print(
            "\nNo matching tasks found."
        )

    else:

        print(
            "\n========== FILTERED TASKS =========="
        )

        for task in tasks:

            print(
                "ID:",
                task[0],
                "| Title:",
                task[1],
                "| Priority:",
                task[2],
                "| Due:",
                task[3],
                "| Status:",
                task[4]
            )

    cursor.close()
    conn.close()


def update_my_task_status(employee_id):

    print(
        "\n========== UPDATE TASK STATUS =========="
    )

    task_id = input(
        "Enter task ID: "
    ).strip()

    if not task_id.isdigit():

        print(
            "Task ID must be a number."
        )

        return

    task_id = int(task_id)

    print("\nSelect new status:")

    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")
    print("4. On Hold")

    choice = input(
        "Enter your choice: "
    ).strip()

    status_map = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed",
        "4": "On Hold"
    }

    if choice not in status_map:

        print(
            "Invalid status choice."
        )

        return

    new_status = status_map[choice]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tasks

    SET status = %s

    WHERE id = %s

      AND EXISTS (
          SELECT 1
          FROM assigned_tasks
          WHERE assigned_tasks.task_id = tasks.id
            AND assigned_tasks.employee_id = %s
      )
    """

    try:

        cursor.execute(
            query,
            (
                new_status,
                task_id,
                employee_id
            )
        )

        conn.commit()

        if cursor.rowcount > 0:

            print(
                "\nTask status updated successfully!"
            )

        else:

            print(
                "\nTask not found or this task is not assigned to you."
            )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not update task status."
        )

        print(
            "Error:",
            e
        )

    cursor.close()
    conn.close()


def view_completed_tasks(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        tasks.id,
        tasks.title,
        tasks.priority,
        tasks.due_date,
        tasks.status
    FROM assigned_tasks

    JOIN tasks
        ON assigned_tasks.task_id = tasks.id

    WHERE assigned_tasks.employee_id = %s
      AND tasks.status = 'Completed'

    ORDER BY tasks.due_date
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    tasks = cursor.fetchall()

    print(
        "\n========== COMPLETED TASKS =========="
    )

    if len(tasks) == 0:

        print(
            "No completed tasks found."
        )

    else:

        for task in tasks:

            print(
                "ID:",
                task[0],
                "| Title:",
                task[1],
                "| Priority:",
                task[2],
                "| Due:",
                task[3],
                "| Status:",
                task[4]
            )

    cursor.close()
    conn.close()


def view_profile(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        name,
        role,
        email,
        created_at
    FROM employees
    WHERE id = %s
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:

        print(
            "\nEmployee profile not found."
        )

    else:

        print(
            "\n========== MY PROFILE =========="
        )

        print(
            "Employee ID:",
            employee[0]
        )

        print(
            "Name:",
            employee[1]
        )

        print(
            "Role:",
            employee[2]
        )

        print(
            "Email:",
            employee[3]
        )

        print(
            "Created At:",
            employee[4]
        )

    cursor.close()
    conn.close()



def update_profile(employee_id):

    print(
        "\n========== UPDATE PROFILE =========="
    )

    name = input(
        "Enter new name: "
    ).strip()

    if name == "":

        print(
            "Name cannot be empty."
        )

        return

    role = input(
        "Enter new role: "
    ).strip()

    if role == "":

        print(
            "Role cannot be empty."
        )

        return

    email = input(
        "Enter new email: "
    ).strip()

    if (
        "@" not in email
        or "." not in email
    ):

        print(
            "Invalid email address."
        )

        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE employees

    SET
        name = %s,
        role = %s,
        email = %s

    WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (
                name,
                role,
                email,
                employee_id
            )
        )

        conn.commit()

        if cursor.rowcount > 0:

            print(
                "\nProfile updated successfully!"
            )

        else:

            print(
                "\nProfile not found."
            )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not update profile."
        )

        print(
            "Error:",
            e
        )

    cursor.close()
    conn.close()


def employee_dashboard(employee_id):

    while True:

        print(
            "\n===================================="
        )

        print(
            "        EMPLOYEE DASHBOARD"
        )

        print(
            "===================================="
        )

        print("1. Dashboard Summary")
        print("2. View My Tasks")
        print("3. View Task Details")
        print("4. Filter My Tasks")
        print("5. Update Task Status")
        print("6. Add Comment")
        print("7. View Task Comments")
        print("8. View Completed Tasks")
        print("9. View Profile")
        print("10. Update Profile")
        print("11. Logout")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            employee_dashboard_summary(
                employee_id
            )

        elif choice == "2":

            show_my_tasks(
                employee_id
            )

        elif choice == "3":

            view_task_details(
                employee_id
            )

        elif choice == "4":

            filter_tasks(
                employee_id
            )

        elif choice == "5":

            update_my_task_status(
                employee_id
            )

        elif choice == "6":

            
            add_comment(
                employee_id
            )

        elif choice == "7":

            
            view_comments(
                employee_id
            )

        elif choice == "8":


            view_completed_tasks(
                employee_id
            )

        elif choice == "9":


            view_profile(
                employee_id
            )

        elif choice == "10":

            update_profile(
                employee_id
            )

        elif choice == "11":

            print(
                "\nLogging out..."
            )

            break

        else:

            print(
                "\nInvalid choice. Please try again."
            )