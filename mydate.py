from datetime import timedelta, date
from abc import ABC, abstractmethod
import csv

class DateDatabase:
    def __init__(self, dates_file='dates.csv'):
        pass
    
    def get_hiring_date(self, employee_id):
        date = self._hiring_dates.get(employee_id)
        if date is None:
            raise ValueError("Invalid employee ID")
        return date
    
    def get_birth_date(self, employee_id):
        date = self._birth_dates.get(employee_id)
        if date is None:
            raise ValueError("Invalid employee ID")
        return date
    
    def get_promotion_date(self, employee_id):
        date = self._promotion_dates.get(employee_id)
        if date is None:
            raise ValueError("Invalid employee ID")
        return date
    
    def display_dates(self, employees):
        print("Employee date info:")
        print("===================")
        for employee in employees:
            print(f"Employee {employee.name} - {employee.calculate_dates(AgeCalculation())}")
            print(f"Employee {employee.name} - {employee.calculate_dates(TenureCalculation())}")
            print(f"Employee {employee.name} - {employee.calculate_dates(DaysUntilPromotionCalculation())}")
        print("")


class MyDate:
    def __init__(self, day=1, month=1, year=2021):
        self.set_date(day, month, year)
    
    def set_date(self, day, month, year):
        if self.is_valid_date(day, month, year):
            self.day = day
            self.month = month
            self.year = year
        else:
            raise ValueError("Invalid date")
    
    @staticmethod
    def is_valid_date(day, month, year):
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if month in {4, 6, 9, 11} and day > 30:
            return False
        if month == 2:
            if MyDate.is_leap_year(year):
                return day <= 29
            else:
                return day <= 28
        return True
    
    @staticmethod
    def is_leap_year(year):
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    
    def date_difference(self, other):
        d1 = date(self.year, self.month, self.day)
        d2 = date(other.year, other.month, other.day)
        return (d1 - d2).days
    
    def __add__(self, days):
        d = date(self.year, self.month, self.day) + timedelta(days=days)
        return MyDate(d.day, d.month, d.year)
    
    def __sub__(self, days):
        d = date(self.year, self.month, self.day) - timedelta(days=days)
        return MyDate(d.day, d.month, d.year)

    def __bool__(self):
        today = date.today()
        current_date = date(self.year, self.month, self.day)
        return current_date >= today
    
    def __str__(self):
        return self.format_date(self.day, self.month, self.year)
    
    @staticmethod
    def format_date(day, month, year, sep="-"):
        return f"{day:02d}{sep}{month:02d}{sep}{year}"
    
    @classmethod
    def set_print_format(cls, sep):
        cls.print_sep = sep
    
    def print_date(self):
        sep = getattr(self, 'print_sep', '-')
        print(self.format_date(self.day, self.month, self.year, sep))

    @classmethod
    def from_string(cls, date_string, sep= "-"):
        year, month, day = map(int, date_string.split(sep))
        return cls(day, month, year)

class DateCalculation(ABC):
    @abstractmethod
    def calculate(self, reference_date, target_date):
        pass

class AgeCalculation(DateCalculation):
    def calculate(self, reference_date, birth_date):
        years = reference_date.year - birth_date.year
        if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
            years -= 1
        return f"Age: {years} years old"
    
class TenureCalculation(DateCalculation):
    def calculate(self, reference_date, hiring_date):
        years = reference_date.year - hiring_date.year
        months = reference_date.month - hiring_date.month
        if months < 0:
            years -= 1
            months += 12
        return f"Tenure: {years} years and {months} months"
    
class DaysUntilPromotionCalculation(DateCalculation):
    def calculate(self, reference_date, promotion_date):
        days = promotion_date.date_difference(reference_date)
        if promotion_date:
            return f"Days until promotion: {days}"
        else:
            return f"Employee was promoted {abs(days)} days ago"
        