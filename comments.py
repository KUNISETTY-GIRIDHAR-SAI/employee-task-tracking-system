from db import get_connection


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

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None



def employee_exists(employee_id):

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

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def employee_assigned_to_task(
    task_id,
    employee_id
):

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
        (
            task_id,
            employee_id
        )
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def add_comment(employee_id=None):

    print(
        "\n========== ADD COMMENT =========="
    )

    if employee_id is None:

        employee_id = input(
            "Enter employee ID: "
        ).strip()

        if not employee_id.isdigit():

            print(
                "Employee ID must be a number."
            )

            return

        employee_id = int(employee_id)


    if not employee_exists(employee_id):

        print(
            "Employee not found."
        )

        return

    task_id = input(
        "Enter task ID: "
    ).strip()

    if not task_id.isdigit():

        print(
            "Task ID must be a number."
        )

        return

    task_id = int(task_id)


    if not task_exists(task_id):

        print(
            "Task not found."
        )

        return


    if not employee_assigned_to_task(
        task_id,
        employee_id
    ):

        print(
            "This employee is not assigned "
            "to this task."
        )

        return


    comment = input(
        "Enter your comment: "
    ).strip()

    if comment == "":

        print(
            "Comment cannot be empty."
        )

        return


    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO comments
    (
        task_id,
        employee_id,
        comment
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
    """

    try:

        cursor.execute(
            query,
            (
                task_id,
                employee_id,
                comment
            )
        )

        conn.commit()

        print(
            "\nComment added successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "\nCould not add comment."
        )

        print(
            "Error:",
            e
        )

    finally:

        cursor.close()
        conn.close()


def view_comments(employee_id=None):

    print(
        "\n========== VIEW COMMENTS =========="
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


    if not task_exists(task_id):

        print(
            "Task not found."
        )

        return


    if employee_id is not None:

        if not employee_assigned_to_task(
            task_id,
            employee_id
        ):

            print(
                "\nYou are not assigned to this task."
            )

            print(
                "You cannot view its comments."
            )

            return


    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        comments.id,
        employees.name,
        comments.comment,
        comments.created_at
    FROM comments

    JOIN employees
        ON comments.employee_id = employees.id

    WHERE comments.task_id = %s

    ORDER BY comments.created_at
    """

    cursor.execute(
        query,
        (task_id,)
    )

    comments = cursor.fetchall()

    if len(comments) == 0:

        print(
            "\nNo comments found for this task."
        )

    else:

        print(
            "\n========== TASK COMMENTS =========="
        )

        for comment in comments:

            print(
                "\nComment ID:",
                comment[0]
            )

            print(
                "Employee:",
                comment[1]
            )

            print(
                "Comment:",
                comment[2]
            )

            print(
                "Created At:",
                comment[3]
            )

    cursor.close()
    conn.close()


def view_employee_comments():

    print(
        "\n========== EMPLOYEE COMMENTS =========="
    )

    employee_id = input(
        "Enter employee ID: "
    ).strip()

    if not employee_id.isdigit():

        print(
            "Employee ID must be a number."
        )

        return

    employee_id = int(employee_id)

    if not employee_exists(employee_id):

        print(
            "Employee not found."
        )

        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        comments.id,
        tasks.title,
        comments.comment,
        comments.created_at
    FROM comments

    JOIN tasks
        ON comments.task_id = tasks.id

    WHERE comments.employee_id = %s

    ORDER BY comments.created_at
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    comments = cursor.fetchall()

    if len(comments) == 0:

        print(
            "\nNo comments found for this employee."
        )

    else:

        for comment in comments:

            print(
                "\nComment ID:",
                comment[0]
            )

            print(
                "Task:",
                comment[1]
            )

            print(
                "Comment:",
                comment[2]
            )

            print(
                "Created At:",
                comment[3]
            )

    cursor.close()
    conn.close()


def comments_menu():

    while True:

        print(
            "\n========== COMMENTS =========="
        )

        print("1. Add Comment")
        print("2. View Task Comments")
        print("3. View Employee Comments")
        print("4. Back")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_comment()

        elif choice == "2":

            view_comments()

        elif choice == "3":

            view_employee_comments()

        elif choice == "4":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )