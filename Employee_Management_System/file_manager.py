import csv
from employee import Employee

FILENAME = "employees.csv"

def load_employees():
    """Load employees from CSV and return a dictionary."""
    employees = {}
    try:
        with open(FILENAME, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                emp = Employee(row["Employee ID"], row["Name"], row["Designation"], row["Salary"], row["Contact"])
                employees[emp.emp_id] = emp
    except FileNotFoundError:
        open(FILENAME, "w").close()  # Create empty file if not found
    return employees

def save_employees(employees):
    """Save employee dictionary to CSV."""
    with open(FILENAME, mode="w", newline="") as file:
        fieldnames = ["Employee ID", "Name", "Designation", "Salary", "Contact"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees.values():
            writer.writerow(emp.to_dict())
