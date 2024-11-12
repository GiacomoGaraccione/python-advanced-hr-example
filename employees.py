from payroll import PayrollCalculator
from productivity import ProductivitySystem
from contacts import AddressBook
from mydate import DateDatabase, MyDate, DateCalculation, AgeCalculation, DaysUntilPromotionCalculation, TenureCalculation
from datetime import date

class EmployeeDatabase:
    def __init__(self):
        self._employees = [
            {"id": 1, "name": "Mary Poppins", "role": "manager"},
            {"id": 2, "name": "John Smith", "role": "secretary"},
            {"id": 3, "name": "Kevin Bacon", "role": "sales"},
            {"id": 4, "name": "Jane Doe", "role": "factory"},
            {"id": 5, "name": "Robin Williams", "role": "secretary"},
        ]
        self.productivity = ProductivitySystem()
        self.payroll = PayrollCalculator()
        self.employee_addresses = AddressBook()
        self.employee_dates = DateDatabase()

    @property
    def employees(self):
        return [self._create_employee(**data) for data in self._employees]

    def _create_employee(self, id, name, role):
        address = self.employee_addresses.get_employee_address(id)
        employee_role = self.productivity.get_role(role)
        payroll_policy = self.payroll.get_policy(id)
        birth_date = self.employee_dates.get_birth_date(id)
        hiring_date = self.employee_dates.get_hiring_date(id)
        promotion_date = self.employee_dates.get_promotion_date(id)
        print(f"Employee {id} - {name} created")
        return Employee(id, name, address, employee_role, payroll_policy, hiring_date, birth_date, promotion_date)
    
    
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
