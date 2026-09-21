class Employee:
    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary

    def get_name(self):
        return self.__name

    def get_salary(self):
        return self.__salary


class Developer(Employee):
    def write_code(self):
        print(f"{self.get_name()} is writing code...")


class Manager(Employee):
    def conduct_meeting(self):
        print(f"{self.get_name()} is conducting meeting...")