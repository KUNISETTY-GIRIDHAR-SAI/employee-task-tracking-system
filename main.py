from login import (
    login,
    users_exist,
    create_first_admin
)

from admin_dashboard import admin_dashboard

from employee_dashboard import employee_dashboard


def main():

    print("\n========================================")
    print("      EMPLOYEE TASK TRACKING SYSTEM")
    print("========================================")


    if not users_exist():

        print("\nNo user accounts found.")

        created = create_first_admin()

        if not created:

            print(
                "\nFirst admin setup was not completed."
            )

            print(
                "Exiting system..."
            )

            return

    while True:

        user = login()

        if user is None:

            print("\nLogin failed.")

            choice = input(
                "Do you want to try again? (yes/no): "
            ).strip().lower()

            if choice == "yes":

                print()

                continue

            else:

                print(
                    "\nExiting system..."
                )

                break

        if user["role"] == "ADMIN":

            print(
                "\nOpening Admin Dashboard..."
            )

            admin_dashboard()


        elif user["role"] == "EMPLOYEE":

            employee_id = user["employee_id"]

            if employee_id is None:

                print(
                    "\nError: This employee account "
                    "is not linked to an employee."
                )

                print(
                    "Please contact the administrator."
                )

                continue

            print(
                "\nOpening Employee Dashboard..."
            )

            employee_dashboard(
                employee_id
            )


        else:

            print(
                "\nInvalid user role."
            )

            continue


        print(
            "\nYou have been logged out."
        )

        choice = input(
            "Do you want to login again? (yes/no): "
        ).strip().lower()

        if choice != "yes":

            print(
                "\nThank you for using the "
                "Employee Task Tracking System."
            )

            break


if __name__ == "__main__":

    main()

    