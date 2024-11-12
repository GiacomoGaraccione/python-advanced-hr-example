from datetime import timedelta, date

class DateDatabase:
    def __init__(self):
        self._hiring_dates = {
            1: MyDate(1, 1, 2021),
            2: MyDate(8, 6, 2022),
            3: MyDate(11, 11, 2024),
            4: MyDate(15, 3, 2023),
            5: MyDate(20, 12, 2021),
        }
        self._birth_dates = {
            1: MyDate(1, 1, 1990),
            2: MyDate(8, 6, 1992),
            3: MyDate(11, 11, 1994),
            4: MyDate(15, 3, 1993),
            5: MyDate(20, 12, 1991),
        }
        self._promotion_dates = {
            1: MyDate(1, 1, 2025),
            2: MyDate(8, 6, 2024),
            3: MyDate(11, 11, 2025),
            4: MyDate(15, 11, 2024),
            5: MyDate(20, 12, 2026),
        }
    
    def get_hiring_date(self, employee_id):
        date = self._hiring_dates.get(employee_id)
        if not date:
            raise ValueError("Invalid employee ID")
        return date
    
    def get_birth_date(self, employee_id):
        date = self._birth_dates.get(employee_id)
        if not date:
            raise ValueError("Invalid employee ID")
        return date
    
    def get_promotion_date(self, employee_id):
        date = self._promotion_dates.get(employee_id)
        if not date:
            raise ValueError("Invalid employee ID")
        return date
    
    def display_dates(self, employees):
        print("Hiring Dates:")
        print("-------------")
        for employee in employees:
            print(f"Employee ID: {employee.name}, Hiring Date: {self.get_hiring_date(employee.id)}")    
        print()
        print("Birth Dates:")
        print("-------------")
        for employee in employees:
            print(f"Employee ID: {employee.name}, Birth Date: {self.get_birth_date(employee.id)}")
        print()
        print("Promotion Dates:")
        print("-------------")
        for employee in employees:
            print(f"Employee ID: {employee.name}, Promotion Date: {self.get_promotion_date(employee.id)}, Days until promotion: {employee.date_until_promotion()}")
        print()



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
    
    def increase_date(self, days):
        d = date(self.year, self.month, self.day) + timedelta(days=days)
        self.set_date(d.day, d.month, d.year)
    
    def decrease_date(self, days):
        d = date(self.year, self.month, self.day) - timedelta(days=days)
        self.set_date(d.day, d.month, d.year)
    
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

date1 = MyDate(1, 1, 2021)
date2 = MyDate(15, 1, 2021)
print(f"Difference in days: {date1.date_difference(date2)}")

date1.increase_date(10)
print(f"Date after increasing 10 days: {date1}")

date1.decrease_date(5)
print(f"Date after decreasing 5 days: {date1}")

MyDate.set_print_format("/")
date1.print_date()
