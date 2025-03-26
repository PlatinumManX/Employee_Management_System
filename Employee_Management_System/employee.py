class Employee:
    def __init__(self, emp_id, name, designation, salary, contact):
        self.emp_id=emp_id
        self.name=name
        self.designation=designation
        self.salary=float(salary)
        self.contact=contact
    def to_dict(self):
        return {
            "Employee ID": self.emp_id,
            "Name": self.name,
            "Designation": self.designation,
            "Salary": self.salary,
            "Contact": self.contact,
        }
    
