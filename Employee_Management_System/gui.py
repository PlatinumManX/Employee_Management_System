import tkinter as tk
from tkinter import messagebox
from file_manager import load_employees, save_employees
from employee import Employee
from analysis import salary_analysis

employees = load_employees()
deleted_employees = []  # Stack for storing deleted employees

def add_employee():
    """Add a new employee from GUI inputs."""
    emp_id = entry_id.get()
    name = entry_name.get()
    designation = entry_designation.get()
    salary = entry_salary.get()
    contact = entry_contact.get()

    if emp_id in employees:
        messagebox.showerror("Error", "Employee ID already exists!")
        return

    employees[emp_id] = Employee(emp_id, name, designation, float(salary), contact)
    save_employees(employees)
    messagebox.showinfo("Success", f"Employee {name} added successfully!")
    update_employee_list()

def update_employee_list():
    """Refresh the listbox to show current employees."""
    listbox.delete(0, tk.END)
    for emp in employees.values():
        listbox.insert(tk.END, f"{emp.emp_id} | {emp.name}")

def view_selected_employee():
    """Show details of the selected employee."""
    try:
        selected_index = listbox.curselection()[0]
        selected_emp_id = listbox.get(selected_index).split(" | ")[0]
        emp = employees[selected_emp_id]

        messagebox.showinfo("Employee Details",
            f"ID: {emp.emp_id}\n"
            f"Name: {emp.name}\n"
            f"Designation: {emp.designation}\n"
            f"Salary: {emp.salary}\n"
            f"Contact: {emp.contact}"
        )
    except IndexError:
        messagebox.showerror("Error", "Please select an employee from the list!")

def delete_selected_employee():
    """Delete the selected employee and store in stack for undo."""
    try:
        selected_index = listbox.curselection()[0]
        selected_emp_id = listbox.get(selected_index).split(" | ")[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Employee {selected_emp_id}?")
        if not confirm:
            return

        deleted_employees.append(employees[selected_emp_id])

        del employees[selected_emp_id]
        save_employees(employees)

        update_employee_list()
        messagebox.showinfo("Success", f"Employee {selected_emp_id} deleted! (Undo available)")

    except IndexError:
        messagebox.showerror("Error", "Please select an employee to delete!")

def restore_last_deleted():
    """Restore the last deleted employee from the stack."""
    if deleted_employees:
        emp = deleted_employees.pop()
        employees[emp.emp_id] = emp
        save_employees(employees)
        update_employee_list()
        messagebox.showinfo("Success", f"Employee {emp.name} restored successfully!")
    else:
        messagebox.showerror("Error", "No recently deleted employees to restore!")

def show_salary_analysis():
    """Display salary analysis in a popup."""
    stats = salary_analysis()
    if not stats:
        messagebox.showerror("Error", "No employees found for salary analysis!")
        return

    messagebox.showinfo("Salary Analysis",
        f"Total Salary Expenditure: {stats['Total Salary']}\n"
        f"Average Salary: {stats['Average Salary']:.2f}\n"
        f"Highest Salary: {stats['Highest Salary']}\n"
        f"Lowest Salary: {stats['Lowest Salary']}"
    )

def search_employee():
    """Search for an employee by ID or Name and display in a popup."""
    query = search_entry.get().strip()

    if not query:
        messagebox.showerror("Error", "Please enter an Employee ID or Name to search!")
        return

    if query in employees:
        emp = employees[query]
        messagebox.showinfo("Employee Found",
            f"ID: {emp.emp_id}\n"
            f"Name: {emp.name}\n"
            f"Designation: {emp.designation}\n"
            f"Salary: {emp.salary}\n"
            f"Contact: {emp.contact}"
        )
        return

    for emp in employees.values():
        if query.lower() in emp.name.lower():
            messagebox.showinfo("Employee Found",
                f"ID: {emp.emp_id}\n"
                f"Name: {emp.name}\n"
                f"Designation: {emp.designation}\n"
                f"Salary: {emp.salary}\n"
                f"Contact: {emp.contact}"
            )
            return

    messagebox.showerror("Not Found", "No employee found with the given ID or Name!")

# Create main GUI window
root = tk.Tk()
root.title("Employee Management System")
root.geometry("400x500")  # Set window size

# Labels and Entry Fields
tk.Label(root, text="Employee ID:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Designation:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_designation = tk.Entry(root)
entry_designation.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Salary:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_salary = tk.Entry(root)
entry_salary.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Contact:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_contact = tk.Entry(root)
entry_contact.grid(row=4, column=1, padx=10, pady=5)

# Buttons with spacing
tk.Button(root, text="Add Employee", command=add_employee).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="View Selected Employee", command=view_selected_employee).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(root, text="Delete Employee", command=delete_selected_employee).grid(row=7, column=0, columnspan=2, pady=5)
tk.Button(root, text="Undo Delete", command=restore_last_deleted).grid(row=8, column=0, columnspan=2, pady=5)

# Search Field and Button
tk.Label(root, text="Search Employee:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
search_entry = tk.Entry(root)
search_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Button(root, text="Search", command=search_employee).grid(row=10, column=0, columnspan=2, pady=5)

# Salary Analysis Button (Moved for better spacing)
tk.Button(root, text="Salary Analysis", command=show_salary_analysis).grid(row=11, column=0, columnspan=2, pady=10)

# Listbox to Display Employees (Wider for better readability)
listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

update_employee_list()
root.mainloop()
