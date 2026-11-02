from db import get_connection

def task_status_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        status,
        COUNT(*) AS total_tasks
    FROM tasks
    GROUP BY status
    ORDER BY status
    """

    cursor.execute(query)

    results = cursor.fetchall()

    print(
        "\n========== TASK STATUS REPORT =========="
    )

    if len(results) == 0:

        print(
            "No task data available."
        )

    else:

        for row in results:

            print(
                "Status:",
                row[0],
                "| Tasks:",
                row[1]
            )

    cursor.close()
    conn.close()


def employee_performance_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        employees.id,
        employees.name,

        COUNT(assigned_tasks.task_id)
            AS total_tasks,

        SUM(tasks.status = 'Completed')
            AS completed_tasks,

        SUM(tasks.status = 'Pending')
            AS pending_tasks,

        SUM(tasks.status = 'In Progress')
            AS in_progress_tasks,

        SUM(tasks.status = 'On Hold')
            AS on_hold_tasks

    FROM employees

    LEFT JOIN assigned_tasks
        ON employees.id = assigned_tasks.employee_id

    LEFT JOIN tasks
        ON assigned_tasks.task_id = tasks.id

    GROUP BY
        employees.id,
        employees.name

    ORDER BY completed_tasks DESC
    """

    cursor.execute(query)

    results = cursor.fetchall()

    print(
        "\n========== EMPLOYEE PERFORMANCE REPORT =========="
    )

    if len(results) == 0:

        print(
            "No employee data available."
        )

    else:

        for row in results:

            total = row[2] or 0

            completed = row[3] or 0

            pending = row[4] or 0

            in_progress = row[5] or 0

            on_hold = row[6] or 0

            if total > 0:

                progress = (
                    completed / total
                ) * 100

            else:

                progress = 0

            print(
                "\nEmployee ID:",
                row[0]
            )

            print(
                "Name:",
                row[1]
            )

            print(
                "Total Tasks:",
                total
            )

            print(
                "Completed:",
                completed
            )

            print(
                "Pending:",
                pending
            )

            print(
                "In Progress:",
                in_progress
            )

            print(
                "On Hold:",
                on_hold
            )

            print(
                "Completion:",
                round(progress, 2),
                "%"
            )

    cursor.close()
    conn.close()


def overdue_task_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        tasks.id,
        tasks.title,
        tasks.priority,
        tasks.due_date,
        tasks.status,

        COALESCE(
            GROUP_CONCAT(
                DISTINCT employees.name
                SEPARATOR ', '
            ),
            'Unassigned'
        ) AS employees

    FROM tasks

    LEFT JOIN assigned_tasks
        ON tasks.id = assigned_tasks.task_id

    LEFT JOIN employees
        ON assigned_tasks.employee_id = employees.id

    WHERE tasks.due_date < CURDATE()
      AND tasks.status != 'Completed'

    GROUP BY
        tasks.id,
        tasks.title,
        tasks.priority,
        tasks.due_date,
        tasks.status

    ORDER BY tasks.due_date
    """

    cursor.execute(query)

    tasks = cursor.fetchall()

    print(
        "\n========== OVERDUE TASK REPORT =========="
    )

    if len(tasks) == 0:

        print(
            "No overdue tasks."
        )

    else:

        for task in tasks:

            print(
                "\nTask ID:",
                task[0]
            )

            print(
                "Title:",
                task[1]
            )

            print(
                "Priority:",
                task[2]
            )

            print(
                "Due Date:",
                task[3]
            )

            print(
                "Status:",
                task[4]
            )

            print(
                "Employees:",
                task[5]
            )

    cursor.close()
    conn.close()


def progress_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        COUNT(*) AS total_tasks,

        SUM(status = 'Completed')
            AS completed_tasks,

        SUM(status = 'Pending')
            AS pending_tasks,

        SUM(status = 'In Progress')
            AS in_progress_tasks,

        SUM(status = 'On Hold')
            AS on_hold_tasks

    FROM tasks
    """

    cursor.execute(query)

    result = cursor.fetchone()

    total = result[0] or 0

    completed = result[1] or 0

    pending = result[2] or 0

    in_progress = result[3] or 0

    on_hold = result[4] or 0

    if total > 0:

        progress = (
            completed / total
        ) * 100

    else:

        progress = 0

    print(
        "\n========== PROGRESS REPORT =========="
    )

    print(
        "Total Tasks:",
        total
    )

    print(
        "Completed:",
        completed
    )

    print(
        "Pending:",
        pending
    )

    print(
        "In Progress:",
        in_progress
    )

    print(
        "On Hold:",
        on_hold
    )

    print(
        "Overall Progress:",
        round(progress, 2),
        "%"
    )

    cursor.close()
    conn.close()


def priority_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        priority,
        COUNT(*) AS total_tasks

    FROM tasks

    GROUP BY priority

    ORDER BY
        FIELD(
            priority,
            'Critical',
            'High',
            'Medium',
            'Low'
        )
    """

    cursor.execute(query)

    results = cursor.fetchall()

    print(
        "\n========== PRIORITY REPORT =========="
    )

    if len(results) == 0:

        print(
            "No task data available."
        )

    else:

        for row in results:

            print(
                "Priority:",
                row[0],
                "| Tasks:",
                row[1]
            )

    cursor.close()
    conn.close()


def generate_reports():

    while True:

        print(
            "\n========================================"
        )

        print(
            "          REPORTS & ANALYTICS"
        )

        print(
            "========================================"
        )

        print("1. Task Status Report")
        print("2. Employee Performance Report")
        print("3. Overdue Task Report")
        print("4. Progress Report")
        print("5. Priority Report")
        print("6. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            task_status_report()

        elif choice == "2":

            employee_performance_report()

        elif choice == "3":

            overdue_task_report()

        elif choice == "4":

            progress_report()

        elif choice == "5":

            priority_report()

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


def reports_menu():

    generate_reports()
