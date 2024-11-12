from payroll import PayrollCalculator
from productivity import ProductivitySystem
from employees import EmployeeDatabase

productivity_system = ProductivitySystem()
payroll_system = PayrollCalculator()
employee_database = EmployeeDatabase()

employees = employee_database.employees
productivity_system.track(employees, 40)
payroll_system.calculate_payroll(employees)
