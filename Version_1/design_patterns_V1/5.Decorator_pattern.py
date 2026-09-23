# ============================================================
# DECORATOR PATTERN
# ============================================================
#
# Definition:
# Decorator Pattern dynamically adds behavior/responsibility
# to an existing object without modifying its class.
#
# CORE IDEA:
#
# Instead of creating many subclasses for every combination,
# wrap objects with decorators.
#
# Example:
#
# BasicCoffee
#     ↓
# MilkDecorator
#     ↓
# SugarDecorator
#     ↓
# WhippedCreamDecorator
#
# ============================================================
# KEY COMPONENTS
# ============================================================
#
# 1. Component
#    → Defines the common interface.
#    → Example: Coffee
#
# 2. Concrete Component
#    → Original/base object.
#    → Example: BasicCoffee, FilterCoffee
#
# 3. Decorator
#    → Wraps a Component.
#    → Follows the same interface.
#
# 4. Concrete Decorator
#    → Adds specific behavior.
#    → Example: MilkDecorator, SugarDecorator
#
# ============================================================
# CORE CONCEPT
# ============================================================
#
# Decorator uses COMPOSITION + SAME INTERFACE.
#
#     self.coffee = coffee
#
# The Decorator:
# - IS-A Coffee
# - HAS-A Coffee
#
# This allows decorators to be stacked.
#
# ============================================================
# WHY USE DECORATOR?
# ============================================================
#
# - Add behavior dynamically.
# - Avoid creating many subclasses.
# - Combine multiple behaviors flexibly.
# - Keep the original class unchanged.
# - Supports Open/Closed Principle.
#
# Without Decorator:
#
#     MilkCoffee
#     SugarCoffee
#     MilkSugarCoffee
#     MilkSugarCreamCoffee
#     ...
#
# With Decorator:
#
#     BasicCoffee
#         ↓
#     MilkDecorator
#         ↓
#     SugarDecorator
#         ↓
#     CreamDecorator
#
# ============================================================
# DECORATOR vs INHERITANCE
# ============================================================
#
# Inheritance:
#     Models an IS-A relationship.
#
#     BasicCoffee IS-A Coffee
#
# Decorator:
#     Uses composition + inheritance.
#
#     MilkDecorator IS-A Coffee
#     MilkDecorator HAS-A Coffee
#
# ============================================================
# DECORATOR vs STRATEGY
# ============================================================
#
# Strategy:
#     Changes HOW something is done.
#
#     Payment → UPI OR Card
#
# Decorator:
#     Adds MORE behavior to an existing object.
#
#     Coffee → Milk + Sugar + Cream
#
# ============================================================
# WHEN TO THINK DECORATOR?
# ============================================================
#
# Look for:
# - Optional features/behavior.
# - Multiple combinations of features.
# - Behavior needs to be added dynamically.
# - Avoid subclass explosion.
#
# Common examples:
# - Coffee toppings
# - Pizza toppings
# - Logging
# - Caching
# - Authentication
# - Compression/Encryption
# - HTTP middleware
#
# ============================================================
# INTERVIEW ONE-LINER:
#
# "Decorator allows us to dynamically add responsibilities
# to an object by wrapping it, without modifying the original
# class."
#
# ============================================================

from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

class BasicCoffee(Coffee):
    def get_description(self):
        return "Basic Coffee"

    def get_price(self):
        return 100

class FilterCoffee(Coffee):
    def get_description(self):
        return "Filter Coffee"

    def get_price(self):
        return 120


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self.coffee = coffee

    def get_description(self):
        return self.coffee.get_description()

    def get_price(self):
        return self.coffee.get_price()


class MilkDecorator(CoffeeDecorator):

    def get_description(self):
        return f"{self.coffee.get_description()} with added Milk"

    def get_price(self):
        return self.coffee.get_price() + 20

class SugarDecorator(CoffeeDecorator):

    def get_description(self):
        return f"{self.coffee.get_description()} with added Sugar"

    def get_price(self):
        return self.coffee.get_price() + 10

class WhippedCreamDecorator(CoffeeDecorator):

    def get_description(self):
        return f"{self.coffee.get_description()} with added Whipped Cream"

    def get_price(self):
        return self.coffee.get_price() + 30

def main():
    coffee = BasicCoffee()
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = MilkDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = SugarDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = WhippedCreamDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())

    print("------------------------------------------")

    coffee = FilterCoffee()
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = MilkDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = SugarDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())

    coffee = WhippedCreamDecorator(coffee)
    print(coffee.get_description())
    print(coffee.get_price())


if __name__ == "__main__":
    main()

