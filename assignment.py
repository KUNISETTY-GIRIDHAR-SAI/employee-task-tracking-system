from db import get_connection


def task_exists(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id
    FROM tasks
    WHERE id = %s
    """

    cursor.execute(query, (task_id,))

    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return task is not None


def employee_exists(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id
    FROM employees
    WHERE id = %s
    """

    cursor.execute(query, (employee_id,))

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return employee is not None


def assignment_exists(task_id, employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id
    FROM assigned_tasks
    WHERE task_id = %s
      AND employee_id = %s
    """

    cursor.execute(
        query,
        (task_id, employee_id)
    )

    assignment = cursor.fetchone()

    cursor.close()
    conn.close()

    return assignment is not None


def assign_task():

    print("\n========== ASSIGN TASK ==========")

    task_id = input(
        "Enter task ID: "
    ).strip()

    if not task_id.isdigit():

        print("Task ID must be a number.")
        return

    task_id = int(task_id)

    if not task_exists(task_id):

        print("Task not found.")
        return

    employee_input = input(
        "Enter employee IDs separated by commas: "
    ).strip()

    if employee_input == "":

        print("Employee ID cannot be empty.")
        return

    employee_ids = employee_input.split(",")

    valid_employee_ids = []

    for employee_id in employee_ids:

        employee_id = employee_id.strip()

        if not employee_id.isdigit():

            print(
                "Invalid employee ID:",
                employee_id
            )
            continue

        employee_id = int(employee_id)

        if not employee_exists(employee_id):

            print(
                "Employee ID",
                employee_id,
                "does not exist."
            )
            continue

        if employee_id not in valid_employee_ids:

            valid_employee_ids.append(
                employee_id
            )

    if len(valid_employee_ids) == 0:

        print(
            "No valid employee IDs were provided."
        )
        return

    conn = get_connection()
    cursor = conn.cursor()

    successful_assignments = 0

    for employee_id in valid_employee_ids:

        if assignment_exists(
            task_id,
            employee_id
        ):

            print(
                "Task is already assigned to employee",
                employee_id
            )

            continue

        query = """
        INSERT INTO assigned_tasks
        (task_id, employee_id)
        VALUES (%s, %s)
        """

        try:

            cursor.execute(
                query,
                (task_id, employee_id)
            )

            successful_assignments += 1

            print(
                "Task assigned to employee",
                employee_id
            )

        except Exception as e:

            print(
                "Could not assign task to employee",
                employee_id
            )

            print("Error:", e)

    if successful_assignments > 0:

        conn.commit()

        print(
            "\nTask assignment completed."
        )

    else:

        conn.rollback()

        print(
            "\nNo new assignments were made."
        )

    cursor.close()
    conn.close()


def view_assignments():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        assigned_tasks.id,
        tasks.id,
        tasks.title,
        employees.id,
        employees.name,
        tasks.priority,
        tasks.due_date,
        tasks.status,
        assigned_tasks.assigned_at
    FROM assigned_tasks
    JOIN tasks
        ON assigned_tasks.task_id = tasks.id
    JOIN employees
        ON assigned_tasks.employee_id = employees.id
    ORDER BY assigned_tasks.id
    """

    cursor.execute(query)

    assignments = cursor.fetchall()

    if len(assignments) == 0:

        print("\nNo task assignments found.")

    else:

        print("\n========== TASK ASSIGNMENTS ==========")

        for assignment in assignments:

            print("\nAssignment ID:", assignment[0])
            print("Task ID:", assignment[1])
            print("Task:", assignment[2])
            print("Employee ID:", assignment[3])
            print("Employee:", assignment[4])
            print("Priority:", assignment[5])
            print("Due Date:", assignment[6])
            print("Status:", assignment[7])
            print("Assigned At:", assignment[8])


    cursor.close()
    conn.close()


def view_employee_assignments():

    employee_id = input(
        "Enter employee ID: "
    ).strip()

    if not employee_id.isdigit():

        print("Employee ID must be a number.")
        return

    employee_id = int(employee_id)

    if not employee_exists(employee_id):

        print("Employee not found.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        tasks.id,
        tasks.title,
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
            "\nNo tasks assigned to this employee."
        )

    else:

        print(
            "\n========== EMPLOYEE ASSIGNMENTS =========="
        )

        for task in tasks:

            print(
                "\nTask ID:", task[0],
                "| Title:", task[1],
                "| Priority:", task[2],
                "| Due:", task[3],
                "| Status:", task[4],
                "| Assigned:", task[5]
            )

    cursor.close()
    conn.close()


def assignment_menu():

    while True:

        print("\n========== TASK ASSIGNMENT ==========")
        print("1. Assign Task")
        print("2. View All Assignments")
        print("3. View Employee Assignments")
        print("4. Back")

        choice = input(
            "Enter your choice: "
        )

        if choice == "1":

            assign_task()

        elif choice == "2":

            view_assignments()

        elif choice == "3":

            view_employee_assignments()

        elif choice == "4":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )