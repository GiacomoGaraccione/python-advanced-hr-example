from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship

Base = declarative_base()

class EmployeeModel(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    address = relationship("AddressModel", uselist=False, back_populates="employee")
    dates = relationship("EmployeeDatesModel", uselist=False, back_populates="employee")
    payroll_policy = relationship("PayrollPolicyModel", uselist=False, back_populates="employee")


class AddressModel(Base):
    __tablename__ = 'addresses'
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    street = Column(String, nullable=False)
    street2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    
    employee = relationship("EmployeeModel", back_populates="address")


class EmployeeDatesModel(Base):
    __tablename__ = 'dates'
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    hiring_date = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    promotion_date = Column(String, nullable=False)
    
    employee = relationship("EmployeeModel", back_populates="dates")


class PayrollPolicyModel(Base):
    __tablename__ = 'policies'
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    policy = Column(String, nullable=False)
    weekly_salary = Column(String, nullable=True)
    hourly_rate = Column(String, nullable=True)
    commission_per_sale = Column(String, nullable=True)
    
    employee = relationship("EmployeeModel", back_populates="payroll_policy")

