from payroll import PayrollCalculator
from productivity import ProductivitySystem
from contacts import AddressBook
from mydate import DateDatabase, MyDate, DateCalculation, AgeCalculation, DaysUntilPromotionCalculation, TenureCalculation
from datetime import date
import csv

class EmployeeDatabase:
    def __init__(self, employees_file="employees.csv"):
        self.productivity = ProductivitySystem()
        self.payroll = PayrollCalculator()
        self.employee_addresses = AddressBook()
        self.employee_dates = DateDatabase()
        self._employees = self._load_employees(employees_file)

    def _load_employees(self, employees_file):
        employees = []
        with open(employees_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                employees.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "role": row["role"]
                })
        return employees

    @property
    def employees(self):
        return [self._create_employee(**data) for data in self._employees]

    def _create_employee(self, id, name, role):
        address = self.employee_addresses.get_employee_address(id)
        employee_role = self.productivity.get_role(role)
        payroll_policy = self.payroll.get_policy(id)
        hiring_date = self.employee_dates.get_hiring_date(id)
        birth_date = self.employee_dates.get_birth_date(id)
        promotion_date = self.employee_dates.get_promotion_date(id)
        print(f"Employee {id} - {name} created")
        return Employee(id, name, address, employee_role, payroll_policy, hiring_date, birth_date, promotion_date)
    
    def add_employee(self, employee_id, name, role):
        new_employee = {"id": employee_id, "name": name, "role": role}
        with open('employees.csv', mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "role"])
            writer.writerow(new_employee)
        print(f"Employee {employee_id} - {name} added successfully.")

    def update_employee(self, employee_id, name=None, role=None):
        updated = False
        employees = []

        with open('employees.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) == employee_id:
                    if name:
                        row["name"] = name
                    if role:
                        if role in ["manager", "secretary", "sales", "factory"]:
                            row["role"] = role
                        else:
                            raise ValueError("Invalid role")
                    updated = True
                employees.append(row)

        if updated:
            with open('employees.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "role"])
                writer.writeheader()
                writer.writerows(employees)
            print(f"Employee {employee_id} updated successfully.")
        else:
            print(f"Employee {employee_id} not found.")

    def delete_employee(self, employee_id):
        deleted = False
        employees = []

        with open('employees.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) != employee_id:
                    employees.append(row)
                else:
                    deleted = True

        if deleted:
            with open('employees.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "role"])
                writer.writeheader()
                writer.writerows(employees)
            print(f"Employee {employee_id} deleted successfully.")
        else:
            print(f"Employee {employee_id} not found.")
    
    
class Employee:
    def __init__(self, id, name, address, role, payroll, hiring_date, birth_date, promotion_date):
        self.id = id
        self.name = name
        self.address = address
        self.role = role
        self.payroll = payroll
        self.hiring_date = hiring_date
        self.birth_date = birth_date
        self.promotion_date = promotion_date

    def work(self, hours):
        duties = self.role.work(hours)
        print(f"Employee {self.id} - {self.name}:")
        print(f"- {duties}")
        print("")
        self.payroll.track_work(hours)

    def calculate_payroll(self):
        return self.payroll.calculate_payroll()
    
    def date_until_promotion(self):
        today = MyDate(date.today().day, date.today().month, date.today().year)
        return self.promotion_date.date_difference(today)
    
    def calculate_dates(self, calculation: DateCalculation):
        if isinstance(calculation, AgeCalculation):
            return calculation.calculate(MyDate(date.today().day, date.today().month, date.today().year), self.birth_date)
        elif isinstance(calculation, DaysUntilPromotionCalculation):
            return calculation.calculate(MyDate(date.today().day, date.today().month, date.today().year), self.promotion_date)
        elif isinstance(calculation, TenureCalculation):
            return calculation.calculate(MyDate(date.today().day, date.today().month, date.today().year), self.hiring_date)
        else:
            return "Unsupported calculation"
