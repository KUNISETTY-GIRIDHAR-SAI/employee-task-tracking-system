from db import get_connection

from employee import (
    add_employee,
    update_employee,
    delete_employee,
    view_employees
)

from task import (
    create_task,
    view_tasks,
    update_task,
    delete_task,
    update_task_status
)

from assignment import (
    assign_task,
    view_assignments
)

from login import user_management_menu

from reports import reports_menu

from dashboard import admin_dashboard_summary


def search_tasks():

    print("\n========== SEARCH TASKS ==========")

    search_text = input(
        "Enter task title or keyword: "
    ).strip()

    if search_text == "":
        print("Search text cannot be empty.")
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
    WHERE
        tasks.title LIKE %s
        OR tasks.description LIKE %s
    GROUP BY
        tasks.id,
        tasks.title,
        tasks.priority,
        tasks.due_date,
        tasks.status
    ORDER BY tasks.due_date
    """

    search_value = "%" + search_text + "%"

    cursor.execute(
        query,
        (search_value, search_value)
    )

    tasks = cursor.fetchall()

    if len(tasks) == 0:

        print("\nNo matching tasks found.")

    else:

        print("\n========== SEARCH RESULTS ==========")

        for task in tasks:

            print("\nTask ID:", task[0])
            print("Title:", task[1])
            print("Priority:", task[2])
            print("Due Date:", task[3])
            print("Status:", task[4])
            print("Employees:", task[5])

    cursor.close()
    conn.close()


def filter_tasks():

    print("\n========== FILTER TASKS ==========")

    print("1. Filter by Status")
    print("2. Filter by Priority")
    print("3. Filter by Employee")
    print("4. Filter by Date Range")
    print("5. Back")

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
            "Enter choice: "
        ).strip()

        status_map = {
            "1": "Pending",
            "2": "In Progress",
            "3": "Completed",
            "4": "On Hold"
        }

        if status_choice not in status_map:

            print("Invalid choice.")

            cursor.close()
            conn.close()

            return

        status = status_map[status_choice]

        query = """
        SELECT
            id,
            title,
            priority,
            due_date,
            status
        FROM tasks
        WHERE status = %s
        ORDER BY due_date
        """

        cursor.execute(
            query,
            (status,)
        )

    
    elif choice == "2":

        print("\n1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Critical")

        priority_choice = input(
            "Enter choice: "
        ).strip()

        priority_map = {
            "1": "Low",
            "2": "Medium",
            "3": "High",
            "4": "Critical"
        }

        if priority_choice not in priority_map:

            print("Invalid choice.")

            cursor.close()
            conn.close()

            return

        priority = priority_map[priority_choice]

        query = """
        SELECT
            id,
            title,
            priority,
            due_date,
            status
        FROM tasks
        WHERE priority = %s
        ORDER BY due_date
        """

        cursor.execute(
            query,
            (priority,)
        )


    elif choice == "3":

        employee_id = input(
            "Enter employee ID: "
        ).strip()

        if not employee_id.isdigit():

            print(
                "Employee ID must be a number."
            )

            cursor.close()
            conn.close()

            return

        query = """
        SELECT
            tasks.id,
            tasks.title,
            tasks.priority,
            tasks.due_date,
            tasks.status,
            employees.name
        FROM assigned_tasks
        JOIN tasks
            ON assigned_tasks.task_id = tasks.id
        JOIN employees
            ON assigned_tasks.employee_id = employees.id
        WHERE employees.id = %s
        ORDER BY tasks.due_date
        """

        cursor.execute(
            query,
            (int(employee_id),)
        )

        tasks = cursor.fetchall()

        if len(tasks) == 0:

            print(
                "\nNo tasks found for this employee."
            )

        else:

            print(
                "\n========== EMPLOYEE TASKS =========="
            )

            for task in tasks:

                print("\nTask ID:", task[0])
                print("Title:", task[1])
                print("Priority:", task[2])
                print("Due Date:", task[3])
                print("Status:", task[4])
                print("Employee:", task[5])

        cursor.close()
        conn.close()

        return


    elif choice == "4":

        start_date = input(
            "Enter start date (YYYY-MM-DD): "
        ).strip()

        end_date = input(
            "Enter end date (YYYY-MM-DD): "
        ).strip()

        query = """
        SELECT
            id,
            title,
            priority,
            due_date,
            status
        FROM tasks
        WHERE due_date BETWEEN %s AND %s
        ORDER BY due_date
        """

        cursor.execute(
            query,
            (start_date, end_date)
        )

    elif choice == "5":

        cursor.close()
        conn.close()

        return

    else:

        print("Invalid choice.")

        cursor.close()
        conn.close()

        return

    tasks = cursor.fetchall()

    if len(tasks) == 0:

        print("\nNo matching tasks found.")

    else:

        print(
            "\n========== FILTER RESULTS =========="
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


def upcoming_task_reminders():

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

    WHERE
        tasks.due_date BETWEEN CURDATE()
        AND DATE_ADD(
            CURDATE(),
            INTERVAL 3 DAY
        )

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
        "\n========== UPCOMING TASK REMINDERS =========="
    )

    if len(tasks) == 0:

        print(
            "No upcoming tasks in the next 3 days."
        )

    else:

        for task in tasks:

            print("\nTask ID:", task[0])
            print("Title:", task[1])
            print("Priority:", task[2])
            print("Due Date:", task[3])
            print("Status:", task[4])
            print("Employees:", task[5])

    cursor.close()
    conn.close()


def employee_management():

    while True:

        print(
            "\n========== EMPLOYEE MANAGEMENT =========="
        )

        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View Employees")
        print("5. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_employee()

        elif choice == "2":

            update_employee()

        elif choice == "3":

            delete_employee()

        elif choice == "4":

            view_employees()

        elif choice == "5":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


def task_management():

    while True:

        print(
            "\n========== TASK MANAGEMENT =========="
        )

        print("1. Create Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Update Task Status")
        print("6. Search Tasks")
        print("7. Filter Tasks")
        print("8. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

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

            search_tasks()

        elif choice == "7":

            filter_tasks()

        elif choice == "8":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )



def assignment_management():

    while True:

        print(
            "\n========== TASK ASSIGNMENT =========="
        )

        print("1. Assign Task")
        print("2. View Assignments")
        print("3. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            assign_task()

        elif choice == "2":

            view_assignments()

        elif choice == "3":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )



def admin_dashboard():

    while True:

        print("\n========================================")
        print("             ADMIN DASHBOARD")
        print("========================================")

        print("1. Dashboard Summary")
        print("2. Employee Management")
        print("3. Task Management")
        print("4. Task Assignment")
        print("5. Reports & Analytics")
        print("6. Upcoming Task Reminders")
        print("7. User Management")
        print("8. Logout")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            admin_dashboard_summary()

        elif choice == "2":

            employee_management()

        elif choice == "3":

            task_management()

        elif choice == "4":

            assignment_management()

        elif choice == "5":

            reports_menu()

        elif choice == "6":

            upcoming_task_reminders()

        elif choice == "7":

            user_management_menu()

        elif choice == "8":

            print(
                "\nLogging out..."
            )

            break

        else:

            print(
                "\nInvalid choice. Please try again."
            )