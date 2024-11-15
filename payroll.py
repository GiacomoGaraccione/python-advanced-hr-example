import csv

class PayrollCalculator():
    def __init__(self):
        pass

    def get_policy(self, employee_id):
        policy = self._employee_policies.get(employee_id)
        if not policy:
            return ValueError(employee_id)
        return policy


    def calculate_payroll(self, employees):
        print("Calculating payroll...")
        for employee in employees:
            print(f"Payroll for {employee.id} - {employee.name}: {employee.calculate_payroll()}")
            if employee.address:
                print(f"Sent to: {employee.address}")
        print("")

    @classmethod
    def create_policy(cls, policy_type, weekly_salary=None, hourly_rate=None, commission_per_sale=None):
        if policy_type == "salary":
            return SalaryPolicy(weekly_salary)
        elif policy_type == "hourly":
            return HourlyPolicy(hourly_rate)
        elif policy_type == "commission":
            return CommissionPolicy(weekly_salary, commission_per_sale)

class PayrollPolicy():
    def __init__(self):
        self.hours_worked = 0

    def track_work(self, hours):
        self.hours_worked += hours
        

class SalaryPolicy(PayrollPolicy):
    def __init__(self, weekly_salary):
        super().__init__()
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary
    
class HourlyPolicy(PayrollPolicy):
    def __init__(self, hour_rate):
        super().__init__()
        self.hour_rate = hour_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hour_rate
    
class CommissionPolicy(SalaryPolicy):
    def __init__(self, weekly_salary, commission_per_sale):
        super().__init__(weekly_salary)
        self.commission_per_sale = commission_per_sale

    @property
    def commission(self):
        sales = self.hours_worked / 5
        return sales * self.commission_per_sale

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission