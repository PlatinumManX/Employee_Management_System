import pandas as pd
import numpy as np
from file_manager import load_employees

def salary_analysis():
    """Analyze salary data and return statistics."""
    employees = load_employees()

    if not employees:
        return None  # Return None if no employees exist

    salaries = np.array([emp.salary for emp in employees.values()])
    
    return {
        "Total Salary": np.sum(salaries),
        "Average Salary": np.mean(salaries),
        "Highest Salary": np.max(salaries),
        "Lowest Salary": np.min(salaries)
    }
