# Employee Task Tracking System

## Project Overview

The Employee Task Tracking System is a Python and MySQL based application designed to manage employees, tasks, task assignments, task progress, comments, reports, and user authentication.

The system provides separate dashboards for administrators and employees with role-based access control.

---

# Technologies Used

- Python
- MySQL
- MySQL Connector/Python
- SQL
- VS Code

---

# Project Structure

```text
EmployeeTaskTrackingSystem/
│
├── main.py
├── db.py
├── login.py
├── employee.py
├── task.py
├── assignment.py
├── comments.py
├── reports.py
├── dashboard.py
├── employee_dashboard.py
├── admin_dashboard.py
└── README.md

## Environment Setup

Create a `.env` file in the project root with your local MySQL credentials:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=employee_task_tracking
```

Do not upload `.env` to GitHub. It is ignored by `.gitignore`.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```
