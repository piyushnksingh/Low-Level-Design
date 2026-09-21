from abc import ABC, abstractmethod


# POLYMORPHISM
#
# Same method: calculate_salary()
# Different implementations behave differently.
#
# Employee defines the common contract.
# Each child class provides its own implementation.


class Employee(ABC):

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def calculate_salary(self):
        pass


class FullTimeEmployee(Employee):

    def __init__(self, name, monthly_salary):
        super().__init__(name)
        self.__monthly_salary = monthly_salary

    def calculate_salary(self):
        # Full-time employees get a fixed monthly salary.
        return self.__monthly_salary


class PartTimeEmployee(Employee):

    def __init__(self, name, hourly_rate, hours_worked):
        super().__init__(name)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    def calculate_salary(self):
        # Part-time salary depends on hours worked.
        return self.__hourly_rate * self.__hours_worked


# Client code depends on Employee abstraction,
# not on FullTimeEmployee or PartTimeEmployee.
#
# This is where polymorphism is clearly visible:
# employee.calculate_salary() calls the appropriate
# implementation depending on the actual object.


def print_salary(employee: Employee):
    print(
        f"{employee.get_name()} earns ₹{employee.calculate_salary()}"
    )


def main():

    employees = [
        FullTimeEmployee("Piyush", 50000),
        PartTimeEmployee("James", 500, 80)
    ]

    for employee in employees:
        print_salary(employee)


if __name__ == "__main__":
    main()


# INTERVIEW NOTES:
#
# Polymorphism:
# Same interface/method call can behave differently
# depending on the actual object.
#
# employee.calculate_salary()
#       ↓
# FullTimeEmployee → fixed monthly salary
# PartTimeEmployee → hourly_rate × hours_worked
#
# Key benefit:
# Client code does not need if/else like:
#
# if employee is FullTime:
#     ...
# elif employee is PartTime:
#     ...
#
# It simply calls:
#
# employee.calculate_salary()
#
# NOTE:
# This example also uses abstraction and inheritance,
# but the main concept being demonstrated is polymorphism.
#
# Abstraction → Defines WHAT should be done.
# Inheritance → Reuses/extends parent class.
# Polymorphism → Same call produces different behavior.