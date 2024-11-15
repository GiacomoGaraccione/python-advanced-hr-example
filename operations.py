from models import EmployeeModel, AddressModel, EmployeeDatesModel, PayrollPolicyModel
from database import get_session
from sqlalchemy.orm.exc import NoResultFound
from mydate import MyDate

def create_employee(name, role):
    session = get_session()
    try:
        existing_employee = session.query(EmployeeModel).filter_by(name=name).one()
        print(f"Employee {name} already exists in the database.")
        return
    except NoResultFound:
        new_employee = EmployeeModel(name=name, role=role)
        session.add(new_employee)
        session.commit()
        print(f"Employee {name} added successfully.")

def get_employee_by_name(name):
    session = get_session()
    employee = session.query(EmployeeModel).filter_by(name=name).one_or_none()
    session.close()
    return employee

def create_employee_address(employee_id, street, city, state, zip_code, street2=None):
    session = get_session()
    try:
        existing_address = session.query(AddressModel).filter_by(employee_id=employee_id).one()
        print(f"Address for employee {employee_id} already exists in the database.")
    except NoResultFound:
        address = AddressModel(employee_id=employee_id, street=street, street2=street2, city=city, state=state, zip_code=zip_code)
        session.add(address)
        print(f"Address for Employee {employee_id} added to the database.")
        session.commit()

def create_employee_dates(employee_id, hiring_date, birth_date, promotion_date):
    session = get_session()
    try:
        existing_dates = session.query(EmployeeDatesModel).filter_by(employee_id=employee_id).one()
        print(f"Dates for employee {employee_id} already exists in the database.")
    except NoResultFound:
        hd = MyDate.from_string(hiring_date)
        bd = MyDate.from_string(birth_date)
        pd = MyDate.from_string(promotion_date)
        if not MyDate.is_valid_date(hd.day, hd.month, hd.year) or not MyDate.is_valid_date(bd.day, bd.month, bd.year) or not MyDate.is_valid_date(pd.day, pd.month, pd.year):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        dates = EmployeeDatesModel(employee_id=employee_id, hiring_date=hiring_date, birth_date=birth_date, promotion_date=promotion_date)
        session.add(dates)
        print(f"Dates for Employee {employee_id} added to the database.")
        session.commit()

def create_employee_policy(employee_id, policy_type, weekly_salary=None, hourly_rate=None, commission_per_sale=None):
    session = get_session()
    try:
        existing_policy = session.query(PayrollPolicyModel).filter_by(employee_id=employee_id).one()
        print(f"Policy for employee {employee_id} already exists in the database.")
    except NoResultFound:
        if policy_type not in ["salary", "hourly", "commission"]:
            raise ValueError("Invalid policy type")
        if weekly_salary:
            weekly_salary = float(weekly_salary)
        if hourly_rate:
            hourly_rate = float(hourly_rate)
        if commission_per_sale:
            commission_per_sale = float(commission_per_sale)
        policy = PayrollPolicyModel(employee_id=employee_id, policy=policy_type, weekly_salary=weekly_salary, hourly_rate=hourly_rate, commission_per_sale=commission_per_sale)
        session.add(policy)
        print(f"Policy for Employee {employee_id} added to the database.")
        session.commit()

def get_all_employees():
    session = get_session()
    employees = session.query(EmployeeModel).all()
    session.close()
    return employees

def get_employee_address(employee_id):
    try:
        session = get_session()
        address = session.query(AddressModel).filter_by(employee_id=employee_id).one()
        session.close()
        return address
    except NoResultFound:
        print(f"Address for employee {employee_id} not found.")
        return None
    
def get_employee_dates(employee_id):
    try:
        session = get_session()
        dates = session.query(EmployeeDatesModel).filter_by(employee_id=employee_id).one()
        session.close()
        return dates
    except NoResultFound:
        print(f"Dates for employee {employee_id} not found.")
        return None

def get_employee_policy(employee_id):
    try:
        session = get_session()
        policy = session.query(PayrollPolicyModel).filter_by(employee_id=employee_id).one()
        session.close()
        return policy
    except NoResultFound:
        print(f"Policy for employee {employee_id} not found.")
        return None
    
def update_employee(employee_id, name=None, role=None):
    session = get_session()
    try:
        employee = session.query(EmployeeModel).filter_by(id=employee_id).one()
        if name:
            employee.name = name
        if role:
            employee.role = role
        session.commit()
        print(f"Employee {employee_id} updated successfully.")
    except NoResultFound:
        print(f"Employee {employee_id} not found in the database.")

def update_employee_dates(employee_id, hiring_date=None, birth_date=None, promotion_date=None):
    session = get_session()
    try:
        dates = session.query(EmployeeDatesModel).filter_by(employee_id=employee_id).one()
        if hiring_date:
            hd = MyDate.from_string(hiring_date)
            if not MyDate.is_valid_date(hd.day, hd.month, hd.year):
                raise ValueError("Invalid hiring date")
            dates.hiring_date = hiring_date
        if birth_date:
            bd = MyDate.from_string(birth_date)
            if not MyDate.is_valid_date(bd.day, bd.month, bd.year):
                raise ValueError("Invalid birth date")
            dates.birth_date = birth_date
        if promotion_date:
            pd = MyDate.from_string(promotion_date)
            if not MyDate.is_valid_date(pd.day, pd.month, pd.year):
                raise ValueError("Invalid promotion date")
            dates.promotion_date = promotion_date
        session.commit()
        print(f"Dates for Employee {employee_id} updated successfully.")
    except NoResultFound:
        print(f"Dates for Employee {employee_id} not found in the database.")

def update_employee_address(employee_id, street=None, city=None, state=None, zip_code=None, street2=None):
    session = get_session()
    try:
        address = session.query(AddressModel).filter_by(employee_id=employee_id).one()
        if street:
            address.street = street
        if street2:
            address.street2 = street2
        if city:
            address.city = city
        if state:
            address.state = state
        if zip_code:
            address.zip_code = zip_code
        session.commit()
        print(f"Address for Employee {employee_id} updated successfully.")
    except NoResultFound:
        print(f"Address for Employee {employee_id} not found in the database.")

def update_employee_policy(employee_id, policy_type, weekly_salary=None, hourly_rate=None, commission_per_sale=None):
    session = get_session()
    try:
        policy = session.query(PayrollPolicyModel).filter_by(employee_id=employee_id).one()
        policy.policy = policy_type
        if policy_type == "salary":
            policy.weekly_salary = float(weekly_salary)
            policy.hourly_rate = None
            policy.commission_per_sale = None
        if policy_type == "hourly":
            policy.hourly_rate = float(hourly_rate)
            policy.weekly_salary = None
            policy.commission_per_sale = None
        if policy_type == "commission":
            policy.commission_per_sale = float(commission_per_sale)
            policy.weekly_salary = float(weekly_salary)
            policy.hourly_rate = None
        session.commit()
        print(f"Policy for Employee {employee_id} updated successfully.")
    except NoResultFound:
        print(f"Policy for Employee {employee_id} not found in the database.")


def delete_employee(employee_id):
    session = get_session()
    try:
        employee = session.query(EmployeeModel).filter_by(id=employee_id).one()
        employee_address = session.query(AddressModel).filter_by(employee_id=employee_id).one()
        employee_dates = session.query(EmployeeDatesModel).filter_by(employee_id=employee_id).one()
        employee_policy = session.query(PayrollPolicyModel).filter_by(employee_id=employee_id).one()
        session.delete(employee_policy)
        session.delete(employee_dates)
        session.delete(employee_address)
        session.delete(employee)
        session.commit()
        print(f"Employee {employee_id} deleted successfully.")
    except NoResultFound:
        print(f"Employee {employee_id} not found in the database.")