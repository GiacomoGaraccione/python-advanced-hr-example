from payroll import PayrollCalculator
from productivity import ProductivitySystem
from employees import EmployeeDatabase
from mydate import DateDatabase
from contacts import AddressBook

productivity_system = ProductivitySystem()
payroll_system = PayrollCalculator()
employee_database = EmployeeDatabase("hr.csv")
date_database = DateDatabase()
address_book = AddressBook()

employees = employee_database.employees

productivity_system.track(employees, 40)
payroll_system.calculate_payroll(employees)
date_database.display_dates(employees)

while True:
    try:
        print("Available options")
        print("1. Insert a new employee")
        print("2. Update an employee's name/role")
        print("3. Update an employee's address")
        print("4. Update an employee's payroll policy")
        print("5. Update an employee's dates")
        print("6. Delete an employee")
        print("7. Exit")
        command = int(input("Enter command: "))
        if command == 1:  
            employee_id = int(input("Enter employee ID:"))
            name = input("Enter name: ")
            role = input("Enter role: ")
            if not role or not name or not employee_id:
                raise ValueError("Invalid input")
            if role not in ["manager", "secretary", "sales", "factory"]:
                raise ValueError("Invalid role")
            employee_database.add_employee(employee_id, name, role)
            hiring_date = input("Enter hiring date (in format YYYY-MM-DD): ")
            birth_date = input("Enter birth date (in format YYYY-MM-DD): ")
            promotion_date = input("Enter promotion date (in format YYYY-MM-DD): ")
            date_database.add_dates(employee_id, hiring_date, birth_date, promotion_date)
            street = input("Enter street: ")
            street2 = input("Enter street2: ")
            city = input("Enter city: ")
            state = input("Enter state: ")
            zip_code = input("Enter zip code: ")
            if not street or not city or not state or not zip_code:
                raise ValueError("Invalid input")
            address_book.add_address(employee_id, street, city, state, zip_code, street2)
            policy = input("Enter policy type (salary, hourly, commission): ")
            if policy not in ["salary", "hourly", "commission"]:
                raise ValueError("Invalid policy type")
            if policy == "salary":
                weekly_salary = float(input("Enter weekly salary:"))
                payroll_system.add_policy(employee_id, policy, weekly_salary=weekly_salary)
            elif policy == "hourly":
                hourly_rate = float(input("Enter hourly rate:"))
                payroll_system.add_policy(employee_id, policy, hourly_rate=hourly_rate)
            elif policy == "commission":
                weekly_salary = float(input("Enter weekly salary:"))
                commission_per_sale = float(input("Enter commission per sale:"))
                payroll_system.add_policy(employee_id, policy, weekly_salary=weekly_salary, commission_per_sale=commission_per_sale)
        elif command == 2:        
            employee_id = int(input("Enter employee ID:"))
            name = input("Enter new name: ")
            role = input("Enter new role: ")
            if not role or not name or not employee_id:
                raise ValueError("Invalid input")
            employee_database.update_employee(employee_id, name, role)
        elif command == 3:
            employee_id = int(input("Enter employee ID:"))
            street = input("Enter street: ")
            street2 = input("Enter street2: ")
            city = input("Enter city: ")
            state = input("Enter state: ")
            zip_code = input("Enter zip code: ")
            address_book.update_address(employee_id, street, city, state, zip_code, street2)
        elif command == 4:
            employee_id = int(input("Enter employee ID:"))
            policy = input("Enter policy type (salary, hourly, commission): ")
            if policy not in ["salary", "hourly", "commission"]:
                raise ValueError("Invalid policy type")
            if policy == "salary":
                weekly_salary = float(input("Enter weekly salary: "))
                payroll_system.update_policy(employee_id, policy, weekly_salary=weekly_salary)
            elif policy == "hourly":
                hourly_rate = float(input("Enter hourly rate: "))
                payroll_system.update_policy(employee_id, policy, hourly_rate=hourly_rate)
            elif policy == "commission":
                weekly_salary = float(input("Enter weekly salary: "))
                commission_per_sale = float(input("Enter commission per sale: "))
                payroll_system.update_policy(employee_id, policy, weekly_salary=weekly_salary, commission_per_sale=commission_per_sale)
        elif command == 5:
            employee_id = int(input("Enter employee ID:"))
            hiring_date = input("Enter hiring date (in format YYYY-MM-DD): ")
            birth_date = input("Enter birth date (in format YYYY-MM-DD): ")
            promotion_date = input("Enter promotion date (in format YYYY-MM-DD): ")
            date_database.update_dates(employee_id, hiring_date, birth_date, promotion_date)
        elif command == 6:
            employee_id = int(input("Enter employee ID:"))
            employee_database.delete_employee(employee_id)
            date_database.delete_dates(employee_id)
            address_book.delete_address(employee_id)
            payroll_system.delete_policy(employee_id)
        elif command == 7:
            print("Exiting...")
            break
        else:
            print("Invalid command. Please try again.")
    except Exception as e:
        print("An error occurred:", str(e))
        continue