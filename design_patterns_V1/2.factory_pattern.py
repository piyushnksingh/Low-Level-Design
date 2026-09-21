# ============================================================
# FACTORY PATTERN
# ============================================================
#
# CORE IDEA:
# Separate OBJECT CREATION from business logic.
#
# Client should not need to know how concrete objects are
# created.
#
#
# ============================================================
# 1. SIMPLE FACTORY
# ============================================================
#
# Definition:
# A single factory creates different types of objects based
# on some input.
#
# Example:
#     NotificationFactory.create_notification("Email")
#
# FLOW:
#
#     Client → Factory → Email / SMS / Push
#
# KEY POINTS:
# - One centralized factory.
# - Factory decides which object to create.
# - Usually uses if/elif or a mapping.
# - Client doesn't directly create concrete objects.
#
# LIMITATION:
# Adding a new type usually requires modifying the factory. -> resolved in factory method
#
# REMEMBER:
# "ONE FACTORY decides WHAT to create."
#
#
# ============================================================
# 2. FACTORY METHOD
# ============================================================
#
# Definition:
# Defines a method for creating an object, but lets subclasses
# decide which concrete object to create.
#
# FLOW:
#
#                 NotificationFactory
#                        │
#                create_notification()
#                        │
#             ┌──────────┼──────────┐
#             ↓          ↓          ↓
#       EmailFactory  SMSFactory  PushFactory
#             ↓          ↓          ↓
#           Email       SMS        Push
#
# KEY POINTS:
# - Uses inheritance.
# - Base factory defines common workflow.
# - Subclasses override the factory method.
# - Each subclass creates its own product.
#
# ADVANTAGE:
# New product → usually add a new factory subclass instead
# of modifying existing factory logic.
#
# REMEMBER:
# "SUBCLASS decides WHAT to create."
#
#
# ============================================================
# 3. ABSTRACT FACTORY
# ============================================================
#
# Definition:
# Provides an interface for creating a FAMILY of related
# objects without specifying their concrete classes.
#
# Example:
#
#     UI Factory
#       ├── create_button()
#       └── create_checkbox()
#
#     LightUIFactory
#       ├── LightButton
#       └── LightCheckbox
#
#     DarkUIFactory
#       ├── DarkButton
#       └── DarkCheckbox
#
# FLOW:
#
#                  UIFactory
#                 /        \
#                /          \
#       LightUIFactory    DarkUIFactory
#           │                  │
#     LightButton         DarkButton
#     LightCheckbox       DarkCheckbox
#
# KEY POINTS:
# - Creates MULTIPLE related objects.
# - Objects created by the factory are designed to work
#   together.
# - Client depends only on the abstract factory.
# - Useful when the system has different PRODUCT FAMILIES.
#
# REMEMBER:
# "ABSTRACT FACTORY creates a FAMILY of related objects."
#
#
# ============================================================
# SIMPLE vs FACTORY METHOD vs ABSTRACT FACTORY
# ============================================================
#
# Simple Factory:
#     One factory
#     → creates different objects
#     → Factory decides
#
# Factory Method:
#     Multiple factory subclasses
#     → each creates a product
#     → Subclass decides
#
# Abstract Factory:
#     Multiple concrete factories
#     → each creates a FAMILY of related products
#
#
# EASY MEMORY TRICK:
#
# Simple Factory
# → ONE factory → ONE type of product at a time
#
# Factory Method
# → SUBCLASS factory → ONE product
#
# Abstract Factory
# → FACTORY FAMILY → PRODUCT FAMILY
#
#
# ============================================================
# QUICK EXAMPLES
# ============================================================
#
# Simple Factory:
#     NotificationFactory
#     → Email / SMS / Push
#
# Factory Method:
#     EmailFactory → Email
#     SMSFactory   → SMS
#     PushFactory  → Push
#
# Abstract Factory:
#     LightUIFactory → LightButton + LightCheckbox
#     DarkUIFactory  → DarkButton + DarkCheckbox
#
#
# ============================================================
# INTERVIEW ONE-LINERS
# ============================================================
#
# Simple Factory:
# "Centralize object creation in one factory."
#
# Factory Method:
# "Let subclasses decide which concrete object to create."
#
# Abstract Factory:
# "Create families of related objects without coupling the
# client to their concrete implementations."
#
# ============================================================




# ---------------------------------------- SIMPLE FACTORY --------------------------------------------------

# from abc import ABC, abstractmethod
#
# class Notification(ABC):
#     @abstractmethod
#     def notify(self):
#         pass
#
# class Email(Notification):
#     def notify(self):
#         print("Email Notification...")
#
# class SMS(Notification):
#     def notify(self):
#         print("SMS Notification...")
#
# class Push(Notification):
#     def notify(self):
#         print("Push Notification...")
#
#
# class NotificationFactory:
#     def create_notification(self, notification_type: str):
#         if notification_type == "Email":
#             return Email()
#         elif notification_type == "SMS":
#             return SMS()
#         elif notification_type == "Push":
#             return Push()
#         else:
#             print("Invalid notification type")
#             return None
#
# class Client:
#     notification_factory = NotificationFactory()
#     notification = notification_factory.create_notification("Email")
#     notification.notify()
#
#     notification = notification_factory.create_notification("SMS")
#     notification.notify()
#
#     notification = notification_factory.create_notification("Push")
#     notification.notify()
#
# if __name__ == "__main__":
#     client = Client()
#


# ---------------------------------------- FACTORY METHOD --------------------------------------------------
# from abc import ABC, abstractmethod
#
# class Notification(ABC):
#     @abstractmethod
#     def notify(self):
#         pass
#
# class Email(Notification):
#     def notify(self):
#         print("Email Notification...")
#
# class SMS(Notification):
#     def notify(self):
#         print("SMS Notification...")
#
# class Push(Notification):
#     def notify(self):
#         print("Push Notification...")
#
#
# class NotificationFactory(ABC):
#     @abstractmethod
#     def create_notification(self):
#         pass
#
#     def send_notification(self):
#         notification = self.create_notification()
#         notification.notify()
#
#
# class EmailFactory(NotificationFactory):
#     def create_notification(self):
#         return Email()
#
# class SMSFactory(NotificationFactory):
#     def create_notification(self):
#         return SMS()
#
# class PushFactory(NotificationFactory):
#     def create_notification(self):
#         return Push()
#
#
# def main():
#     EmailFactory().send_notification()
#     SMSFactory().send_notification()
#     PushFactory().send_notification()
#
#
# if __name__ == "__main__":
#     main()


# ---------------------------------------- ABSTRACT FACTORY --------------------------------------------------

from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class WindowsButton(Button):
    def render(self):
        print("Windows Button...")

class MacButton(Button):
    def render(self):
        print("Mac Button...")


class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

class WindowsCheckbox(Checkbox):
    def render(self):
        print("Windows Checkbox...")

class MacCheckbox(Checkbox):
    def render(self):
        print("Mac Checkbox...")


class UIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass

class WindowsUIFactory(UIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()

class MacUIFactory(UIFactory):
    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()


def render_ui(factory: UIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.render()
    checkbox.render()

def main():
    render_ui(WindowsUIFactory())
    print("----------------------------")
    render_ui(MacUIFactory())

if __name__ == "__main__":
    main()