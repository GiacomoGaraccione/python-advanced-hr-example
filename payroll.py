import csv

class PayrollCalculator():
    def __init__(self, policies_file="policies.csv"):
        self._employee_policies = self._load_policies(policies_file)

    def _load_policies(self, policies_file):
        policies = {}
        with open(policies_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                emp_id = int(row["id"])
                policy_type = row["policy"]
                if policy_type == "salary":
                    policies[emp_id] = SalaryPolicy(float(row["weekly_salary"]))
                elif policy_type == "hourly":
                    policies[emp_id] = HourlyPolicy(float(row["hourly_rate"]))
                elif policy_type == "commission":
                    policies[emp_id] = CommissionPolicy(float(row["weekly_salary"]), float(row["commission_per_sale"]))
        return policies

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

    def add_policy(self, employee_id, policy_type, weekly_salary=None, hourly_rate=None, commission_per_sale=None):
        new_policy = {
            "id": employee_id,
            "policy_type": policy_type,
            "weekly_salary": weekly_salary or '',
            "hourly_rate": hourly_rate or '',
            "commission_per_sale": commission_per_sale or ''
        }
        with open('policies.csv', mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "policy_type", "weekly_salary", "hourly_rate", "commission_per_sale"])
            writer.writerow(new_policy)
        print(f"Payroll policy for Employee {employee_id} added successfully.")

    def update_policy(self, employee_id, policy_type=None, weekly_salary=None, hourly_rate=None, commission_per_sale=None):
        updated = False
        policies = []

        with open('policies.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) == employee_id:
                    if policy_type:
                        row["policy"] = policy_type
                    if policy_type == "salary":
                        row["weekly_salary"] = float(weekly_salary)
                        row["hourly_rate"] = None
                        row["commission_per_sale"] = None
                    if policy_type == "hourly":
                        row["hourly_rate"] = float(hourly_rate)
                        row["weekly_salary"] = None
                        row["commission_per_sale"] = None
                    if policy_type == "commission":
                        row["commission_per_sale"] = float(commission_per_sale)
                        row["weekly_salary"] = float(weekly_salary)
                        row["hourly_rate"] = None
                    updated = True
                policies.append(row)

        if updated:
            with open('policies.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "policy", "weekly_salary", "hourly_rate", "commission_per_sale"])
                writer.writeheader()
                writer.writerows(policies)
            print(f"Payroll policy for Employee {employee_id} updated successfully.")
        else:
            print(f"Payroll policy for Employee {employee_id} not found.")

    def delete_policy(self, employee_id):
        deleted = False
        policies = []

        with open('policies.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) != employee_id:
                    policies.append(row)
                else:
                    deleted = True

        if deleted:
            with open('policies.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "policy", "weekly_salary", "hourly_rate", "commission_per_sale"])
                writer.writeheader()
                writer.writerows(policies)
            print(f"Payroll policy for Employee {employee_id} deleted successfully.")
        else:
            print(f"Payroll policy for Employee {employee_id} not found.")

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