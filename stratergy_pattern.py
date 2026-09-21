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

# --- Strategy Interface for Walk ---
class WalkableRobot(ABC):
    @abstractmethod
    def walk(self):
        pass

# --- Concrete Strategies for Walk ---
class NormalWalk(WalkableRobot):
    def walk(self):
        print("Walking normally...")

class NoWalk(WalkableRobot):
    def walk(self):
        print("Cannot walk.")


# --- Strategy Interface for Talk ---
class TalkableRobot(ABC):
    @abstractmethod
    def talk(self):
        pass

# --- Concrete Strategies for Talk ---
class NormalTalk(TalkableRobot):
    def talk(self):
        print("Talking normally...")

class NoTalk(TalkableRobot):
    def talk(self):
        print("Cannot talk.")


# --- Strategy Interface for Fly ---
class FlyableRobot(ABC):
    @abstractmethod
    def fly(self):
        pass

# --- Concrete Strategies for Fly ---
class NormalFly(FlyableRobot):
    def fly(self):
        print("Flying normally...")

class NoFly(FlyableRobot):
    def fly(self):
        print("Cannot fly.")


# --- Robot Base Class ---
class Robot(ABC):
    def __init__(self, walk_behavior, talk_behavior, fly_behavior):
        self.walk_behavior = walk_behavior
        self.talk_behavior = talk_behavior
        self.fly_behavior = fly_behavior

    def walk(self):
        self.walk_behavior.walk()

    def talk(self):
        self.talk_behavior.talk()

    def fly(self):
        self.fly_behavior.fly()

    @abstractmethod
    def projection(self):
        pass


# --- Concrete Robot Types ---
class CompanionRobot(Robot):
    def projection(self):
        print("Displaying friendly companion features...")


class WorkerRobot(Robot):
    def projection(self):
        print("Displaying worker efficiency stats...")


# --- Main ---
if __name__ == "__main__":
    robot1 = CompanionRobot(NormalWalk(), NormalTalk(), NoFly())
    robot1.walk()
    robot1.talk()
    robot1.fly()
    robot1.projection()

    print("--------------------")

    robot2 = WorkerRobot(NoWalk(), NoTalk(), NormalFly())
    robot2.walk()
    robot2.talk()
    robot2.fly()
    robot2.projection()