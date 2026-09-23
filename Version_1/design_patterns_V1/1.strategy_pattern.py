# ============================================================
# STRATEGY PATTERN
# ============================================================
#
# Definition:
# Strategy Pattern defines a family of interchangeable
# algorithms/behaviors and allows us to switch between them
# without changing the Context.
#
#
# CORE IDEA:
#
# Instead of:
#
# if type == "A":
#     logic A
# elif type == "B":
#     logic B
#
# Create separate strategy classes:
#
#                 Strategy
#                    ↑
#              ┌─────┼─────┐
#              A     B     C
#
#
# KEY COMPONENTS:
#
# 1. Strategy
#    → Defines the common interface/contract.
#
# 2. Concrete Strategies
#    → Provide different implementations/algorithms.
#
# 3. Context
#    → Uses the selected strategy.
#
# In our example:
#
# DeliveryStrategy → Strategy
# Standard/Express/SameDay → Concrete Strategies
# DeliveryService → Context
#
#
# WHY USE STRATEGY?
#
# - Avoid large if/elif blocks.
# - Separate different algorithms/behaviors.
# - Easily add new behavior.
# - Change behavior without modifying the Context.
# - Reduce coupling.
#
#
# OCP CONNECTION:
#
# Adding a new strategy should not require modifying
# the existing Context.
#
# Example:
#
# class PremiumDelivery(DeliveryStrategy):
#     ...
#
# We add a new class instead of modifying DeliveryService.
#
# Therefore, Strategy Pattern naturally supports
# the Open/Closed Principle.
#
#
# STRATEGY vs POLYMORPHISM:
#
# Polymorphism:
#     → OOP mechanism.
#
# Strategy Pattern:
#     → Uses polymorphism to make behavior interchangeable.
#
#
# STRATEGY vs INHERITANCE:
#
# Inheritance:
#     → Models an "IS-A" relationship.
#
# Strategy:
#     → Models interchangeable "HOW" behavior.
#
# Example:
#
# Developer IS-A Employee       → Inheritance
# UPI is a WAY to make payment   → Strategy
#
#
# WHEN TO THINK STRATEGY?
#
# Look for:
# - Multiple ways of doing something.
# - Different algorithms.
# - Behavior that can change.
# - Large if/else based on type.
#
# Common examples:
# - Payment methods
# - Delivery methods
# - Discount calculation
# - Tax calculation
# - Notification methods
# - Route calculation
# - Authentication methods
#
#
# INTERVIEW ONE-LINER:
#
# "I use Strategy when I have multiple interchangeable ways
# of performing an operation and want to switch between them
# without changing the Context."
#
# ============================================================

from abc import ABC, abstractmethod

class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate_fee(self):
        pass


class StandardDelivery(DeliveryStrategy):
    def calculate_fee(self):
        return 50

class ExpressDelivery(DeliveryStrategy):
    def calculate_fee(self):
        return 100

class SameDayDelivery(DeliveryStrategy):
    def calculate_fee(self):
        return 200


class DeliveryService():
    def __init__(self, delivery_strategy : DeliveryStrategy):
        self.delivery_strategy = delivery_strategy

    def calculate_fee(self):
        return self.delivery_strategy.calculate_fee()


class Client:
    service_1 = DeliveryService(StandardDelivery())
    print(service_1.calculate_fee())

    service_2 = DeliveryService(ExpressDelivery())
    print(service_2.calculate_fee())

    service_3 = DeliveryService(SameDayDelivery())
    print(service_3.calculate_fee())


if __name__ == "__main__":
    Client()



