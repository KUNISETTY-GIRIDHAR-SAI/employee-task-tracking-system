from db import get_connection


def valid_email(email):
    return "@" in email and "." in email


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


def add_employee():

    print("\n========== ADD EMPLOYEE ==========")

    name = input("Enter employee name: ").strip()

    if name == "":
        print("Employee name cannot be empty.")
        return

    role = input("Enter employee role: ").strip()

    if role == "":
        print("Employee role cannot be empty.")
        return

    email = input("Enter employee email: ").strip()

    if not valid_email(email):
        print("Invalid email address.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO employees
    (name, role, email)
    VALUES (%s, %s, %s)
    """

    try:

        cursor.execute(
            query,
            (name, role, email)
        )

        conn.commit()

        print("\nEmployee added successfully!")
        print("Employee ID:", cursor.lastrowid)

    except Exception as e:

        conn.rollback()

        print("\nCould not add employee.")
        print("Error:", e)

    cursor.close()
    conn.close()


def update_employee():

    print("\n========== UPDATE EMPLOYEE ==========")

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

    name = input(
        "Enter new employee name: "
    ).strip()

    if name == "":
        print("Employee name cannot be empty.")
        return

    role = input(
        "Enter new employee role: "
    ).strip()

    if role == "":
        print("Employee role cannot be empty.")
        return

    email = input(
        "Enter new employee email: "
    ).strip()

    if not valid_email(email):

        print("Invalid email address.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE employees
    SET name = %s,
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
                "\nEmployee updated successfully!"
            )
        else:
            print("\nNo changes were made.")

    except Exception as e:

        conn.rollback()

        print("\nCould not update employee.")
        print("Error:", e)

    cursor.close()
    conn.close()


def delete_employee():

    print("\n========== DELETE EMPLOYEE ==========")

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

    confirm = input(
        "Are you sure you want to delete this employee? (yes/no): "
    ).lower()

    if confirm != "yes":

        print("Employee deletion cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    DELETE FROM employees
    WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (employee_id,)
        )

        conn.commit()

        print(
            "\nEmployee deleted successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not delete employee."
        )
        print("Error:", e)

    cursor.close()
    conn.close()


def view_employees():

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
    ORDER BY id
    """

    cursor.execute(query)

    employees = cursor.fetchall()

    if len(employees) == 0:

        print("\nNo employees found.")

    else:

        print("\n========== EMPLOYEE LIST ==========")

        for employee in employees:

            print("\nEmployee ID:", employee[0])
            print("Name:", employee[1])
            print("Role:", employee[2])
            print("Email:", employee[3])
            print("Created At:", employee[4])


    cursor.close()
    conn.close()


def employee_menu():

    while True:

        print("\n========== EMPLOYEE MANAGEMENT ==========")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View Employees")
        print("5. Back")

        choice = input(
            "Enter your choice: "
        )

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