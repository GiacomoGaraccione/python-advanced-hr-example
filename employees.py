from payroll import PayrollCalculator
from productivity import ProductivitySystem
from contacts import AddressBook, Address
from mydate import DateDatabase, MyDate, DateCalculation, AgeCalculation, DaysUntilPromotionCalculation, TenureCalculation
from datetime import date
import csv
import operations

class EmployeeDatabase:
    def __init__(self, data_file="hr.csv"):
        self.productivity = ProductivitySystem()
        self.payroll = PayrollCalculator()
        self.employee_addresses = AddressBook()
        self.employee_dates = DateDatabase()
        self._employees = self._load_employees(data_file)

    def _load_employees(self, data_file):
        employees = []
        with open(data_file, newline='') as csvfile:
            try:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    operations.create_employee(row["name"], row["role"])
                    employee_id = operations.get_employee_by_name(row["name"]).id
                    operations.create_employee_address(employee_id, row["street"], row["city"], row["state"], row["zip_code"], row.get("street2", None))
                    operations.create_employee_dates(employee_id, row["hiring_date"], row["birth_date"], row["promotion_date"])
                    operations.create_employee_policy(employee_id, row["policy"], row.get("weekly_salary", None), row.get("hourly_rate", None), row.get("commission_per_sale", None))
                
                all_emps = operations.get_all_employees()
                for employee_record in all_emps:
                    employee_id = employee_record.id
                    name = employee_record.name
                    role = employee_record.role

                    address_record = operations.get_employee_address(employee_id)
                    address = None
                    if address_record:
                        address = Address(
                            street=address_record.street,
                            street2=address_record.street2,
                            city=address_record.city,
                            state=address_record.state,
                            zip_code=address_record.zip_code
                        )
                    dates_record = operations.get_employee_dates(employee_id)
                    hiring_date = birth_date = promotion_date = None
                    if dates_record:
                        hiring_date = MyDate.from_string(dates_record.hiring_date)
                        birth_date = MyDate.from_string(dates_record.birth_date)
                        promotion_date = MyDate.from_string(dates_record.promotion_date)

                    policy_record = operations.get_employee_policy(employee_id)
                    payroll_policy = None
                    if policy_record:
                        payroll_policy = PayrollCalculator.create_policy(
                            policy_type=policy_record.policy,
                            weekly_salary=policy_record.weekly_salary,
                            hourly_rate=policy_record.hourly_rate,
                            commission_per_sale=policy_record.commission_per_sale
                        )
                    role = self.productivity.get_role(role)
                    employee = Employee(employee_id, name, address, role, payroll_policy, hiring_date, birth_date, promotion_date)
                    employees.append(employee)    
            except ValueError as e:
                print(f"Error: {e}")
        return employees

    @property
    def employees(self):
        return self._employees
    
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

    def __str__(self):
        return f"Employee {self.id} - {self.name}\nAddress: {self.address}\nRole: {self.role}\nPayroll: {self.payroll}\nHiring Date: {self.hiring_date}\nBirth Date: {self.birth_date}\nPromotion Date: {self.promotion_date}"


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
