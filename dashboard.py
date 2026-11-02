from db import get_connection


def get_dashboard_data():
    """
    Get the main dashboard statistics.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    )

    total_employees = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Completed'
        """
    )

    completed_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Pending'
        """
    )

    pending_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'In Progress'
        """
    )

    in_progress_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'On Hold'
        """
    )

    on_hold_tasks = cursor.fetchone()[0]

    if total_tasks > 0:

        progress = (
            completed_tasks / total_tasks
        ) * 100

    else:

        progress = 0

    cursor.close()
    conn.close()

    return {
        "total_employees": total_employees,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "on_hold_tasks": on_hold_tasks,
        "progress": round(progress, 2)
    }


def admin_dashboard_summary():
    """
    Display dashboard information for admin.
    """

    data = get_dashboard_data()

    print("\n========================================")
    print("           ADMIN DASHBOARD")
    print("========================================")

    print(
        "Total Employees :",
        data["total_employees"]
    )

    print(
        "Total Tasks     :",
        data["total_tasks"]
    )

    print(
        "Completed Tasks :",
        data["completed_tasks"]
    )

    print(
        "Pending Tasks   :",
        data["pending_tasks"]
    )

    print(
        "In Progress     :",
        data["in_progress_tasks"]
    )

    print(
        "On Hold         :",
        data["on_hold_tasks"]
    )

    print(
        "Overall Progress:",
        data["progress"],
        "%"
    )


def employee_dashboard_summary(employee_id):
    """
    Display dashboard information
    for a particular employee.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        COUNT(*) AS total_tasks,

        SUM(tasks.status = 'Pending')
            AS pending_tasks,

        SUM(tasks.status = 'In Progress')
            AS in_progress_tasks,

        SUM(tasks.status = 'Completed')
            AS completed_tasks,

        SUM(tasks.status = 'On Hold')
            AS on_hold_tasks

    FROM assigned_tasks

    JOIN tasks
        ON assigned_tasks.task_id = tasks.id

    WHERE assigned_tasks.employee_id = %s
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    result = cursor.fetchone()

    total_tasks = result[0] or 0
    pending_tasks = result[1] or 0
    in_progress_tasks = result[2] or 0
    completed_tasks = result[3] or 0
    on_hold_tasks = result[4] or 0

    if total_tasks > 0:

        progress = (
            completed_tasks / total_tasks
        ) * 100

    else:

        progress = 0

    print("\n========================================")
    print("        EMPLOYEE DASHBOARD SUMMARY")
    print("========================================")

    print(
        "Total Assigned Tasks :",
        total_tasks
    )

    print(
        "Pending Tasks        :",
        pending_tasks
    )

    print(
        "In Progress Tasks    :",
        in_progress_tasks
    )

    print(
        "Completed Tasks      :",
        completed_tasks
    )

    print(
        "On Hold Tasks        :",
        on_hold_tasks
    )

    print(
        "Overall Progress     :",
        round(progress, 2),
        "%"
    )

    cursor.close()
    conn.close()


def dashboard_menu():

    while True:

        print("\n========== DASHBOARD ==========")

        print("1. Admin Dashboard")
        print("2. Employee Dashboard Summary")
        print("3. Back")

        choice = input(
            "Enter your choice: "
        )

        if choice == "1":

            admin_dashboard_summary()

        elif choice == "2":

            employee_id = input(
                "Enter employee ID: "
            ).strip()

            if not employee_id.isdigit():

                print(
                    "Employee ID must be a number."
                )

                continue

            employee_dashboard_summary(
                int(employee_id)
            )

        elif choice == "3":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )