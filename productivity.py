class ProductivitySystem():

    def __init__(self):
        self._roles = {
            "manager": ManagerRole,
            "secretary": SecretaryRole,
            "sales": SalesRole,
            "factory": FactoryRole
        }

    def get_role(self, role_id):
        role_type = self._roles.get(role_id)
        if not role_type:
            raise ValueError("role_id")
        return role_type()


    def track(self, employees, hours):
        print("Tracking employee productivity...")
        for employee in employees:
            result = employee.work(hours)
            print(f"{employee.name}: {result}")
        print("")

class ManagerRole():
    def work(self, hour):
        return f"told people what to do for {hour} hours"

class SecretaryRole():
    def work(self, hour):
        return f"did paperwork for {hour} hours"

class SalesRole():
    def work(self, hour):
        return f"sold products for {hour} hours"

class FactoryRole():
    def work(self, hour):
        return f"manufactured products for {hour} hours"