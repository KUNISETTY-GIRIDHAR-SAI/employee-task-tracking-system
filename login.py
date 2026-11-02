import hashlib
import secrets

from db import get_connection


def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(password, stored_hash):

    try:

        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        stored_password_hash = bytes.fromhex(
            hash_hex
        )

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return secrets.compare_digest(
            password_hash,
            stored_password_hash
        )

    except (ValueError, TypeError):

        return False


def users_exist():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM users
    """

    cursor.execute(query)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


def username_exists(username):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT user_id
    FROM users
    WHERE username = %s
    """

    cursor.execute(
        query,
        (username,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def create_first_admin():

    print("\n========================================")
    print("          FIRST ADMIN SETUP")
    print("========================================")

    print(
        "No users exist in the system."
    )

    print(
        "Create the first administrator account."
    )

    username = input(
        "\nEnter admin username: "
    ).strip()

    if username == "":

        print(
            "Username cannot be empty."
        )

        return False

    if username_exists(username):

        print(
            "Username already exists."
        )

        return False

    password = input(
        "Enter admin password: "
    )

    if password == "":

        print(
            "Password cannot be empty."
        )

        return False

    if len(password) < 6:

        print(
            "Password must contain at least 6 characters."
        )

        return False

    password_hash = hash_password(
        password
    )

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users
    (
        employee_id,
        username,
        password_hash,
        role,
        status
    )
    VALUES
    (
        NULL,
        %s,
        %s,
        'ADMIN',
        'Active'
    )
    """

    try:

        cursor.execute(
            query,
            (
                username,
                password_hash
            )
        )

        conn.commit()

        print(
            "\nFirst admin account created successfully!"
        )

        print(
            "You can now login."
        )

        return True

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not create admin account."
        )

        print(
            "Error:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()


def create_user():

    print(
        "\n========== CREATE USER =========="
    )

    username = input(
        "Enter username: "
    ).strip()

    if username == "":

        print(
            "Username cannot be empty."
        )

        return

    if username_exists(username):

        print(
            "Username already exists."
        )

        return

    password = input(
        "Enter password: "
    )

    if password == "":

        print(
            "Password cannot be empty."
        )

        return

    if len(password) < 6:

        print(
            "Password must contain at least 6 characters."
        )

        return

    print("\nSelect role:")

    print("1. Admin")
    print("2. Employee")

    role_choice = input(
        "Enter your choice: "
    ).strip()

    if role_choice == "1":

        role = "ADMIN"

        employee_id = None

    elif role_choice == "2":

        role = "EMPLOYEE"

        employee_id = input(
            "Enter employee ID for this user: "
        ).strip()

        if not employee_id.isdigit():

            print(
                "Employee ID must be a number."
            )

            return

        employee_id = int(employee_id)

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id
        FROM employees
        WHERE id = %s
        """

        cursor.execute(
            query,
            (employee_id,)
        )

        employee = cursor.fetchone()

        cursor.close()
        conn.close()

        if employee is None:

            print(
                "Employee ID not found."
            )

            return

    else:

        print(
            "Invalid role choice."
        )

        return

    password_hash = hash_password(
        password
    )

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users
    (
        employee_id,
        username,
        password_hash,
        role
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    """

    try:

        cursor.execute(
            query,
            (
                employee_id,
                username,
                password_hash,
                role
            )
        )

        conn.commit()

        print(
            "\nUser created successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not create user."
        )

        print(
            "Error:",
            e
        )

    finally:

        cursor.close()
        conn.close()


def login():

    print("\n====================================")
    print("       EMPLOYEE TASK SYSTEM")
    print("              LOGIN")
    print("====================================")

    username = input(
        "Username: "
    ).strip()

    password = input(
        "Password: "
    )

    if username == "" or password == "":

        print(
            "\nUsername and password are required."
        )

        return None

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        user_id,
        employee_id,
        username,
        password_hash,
        role,
        status
    FROM users
    WHERE username = %s
    """

    cursor.execute(
        query,
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:

        print(
            "\nInvalid username or password."
        )

        return None

    user_id = user[0]
    employee_id = user[1]
    username = user[2]
    stored_password_hash = user[3]
    role = user[4]
    status = user[5]

    if not verify_password(
        password,
        stored_password_hash
    ):

        print(
            "\nInvalid username or password."
        )

        return None

    if status != "Active":

        print(
            "\nYour account is inactive."
        )

        print(
            "Please contact the administrator."
        )

        return None

    print(
        "\nLogin successful!"
    )

    print(
        "Welcome,",
        username
    )

    return {
        "user_id": user_id,
        "employee_id": employee_id,
        "username": username,
        "role": role,
        "status": status
    }


def change_user_status():

    print(
        "\n========== CHANGE USER STATUS =========="
    )

    username = input(
        "Enter username: "
    ).strip()

    if username == "":

        print(
            "Username cannot be empty."
        )

        return

    print("\nSelect account status:")

    print("1. Active")
    print("2. Inactive")

    choice = input(
        "Enter your choice: "
    ).strip()

    if choice == "1":

        status = "Active"

    elif choice == "2":

        status = "Inactive"

    else:

        print(
            "Invalid choice."
        )

        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE users
    SET status = %s
    WHERE username = %s
    """

    try:

        cursor.execute(
            query,
            (
                status,
                username
            )
        )

        conn.commit()

        if cursor.rowcount > 0:

            print(
                "\nUser status updated successfully!"
            )

        else:

            print(
                "\nUser not found."
            )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not update user status."
        )

        print(
            "Error:",
            e
        )

    finally:

        cursor.close()
        conn.close()


def view_users():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        user_id,
        employee_id,
        username,
        role,
        status
    FROM users
    ORDER BY user_id
    """

    cursor.execute(query)

    users = cursor.fetchall()

    if len(users) == 0:

        print(
            "\nNo users found."
        )

    else:

        print(
            "\n========== USER LIST =========="
        )

        for user in users:

            print(
                "\nUser ID:",
                user[0]
            )

            print(
                "Employee ID:",
                user[1]
            )

            print(
                "Username:",
                user[2]
            )

            print(
                "Role:",
                user[3]
            )

            print(
                "Status:",
                user[4]
            )

    cursor.close()
    conn.close()


def user_management_menu():

    while True:

        print(
            "\n========== USER MANAGEMENT =========="
        )

        print("1. Create User")
        print("2. View Users")
        print("3. Change User Status")
        print("4. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            create_user()

        elif choice == "2":

            view_users()

        elif choice == "3":

            change_user_status()

        elif choice == "4":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )

def logout():

    print(
        "\n===================================="
    )

    print(
        "          LOGGING OUT"
    )

    print(
        "===================================="
    )

    print(
        "You have been logged out successfully."
    )