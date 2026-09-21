# ============================================================
# ADAPTER PATTERN
# ============================================================
#
# Definition:
# Adapter Pattern converts the interface of an existing class
# into an interface expected by the client.
#
# In simple words:
# Adapter = INTERFACE TRANSLATOR
#
# ============================================================
# CORE IDEA
# ============================================================
#
# Client expects:
#
#     send(message)
#
# Existing/Third-party class provides:
#
#     send_sms(phone_number, message)
#
# Adapter translates between them.
#
#     Client
#       ↓
# NotificationService
#       ↓
# TwilioAdapter
#       ↓
# Twilio
#
# ============================================================
# KEY COMPONENTS
# ============================================================
#
# 1. Target
#    → Interface expected by the client.
#    → Example: NotificationService
#
# 2. Adaptee
#    → Existing class with an incompatible interface.
#    → Example: Twilio
#
# 3. Adapter
#    → Converts Adaptee's interface into Target's interface.
#    → Example: TwilioAdapter
#
# 4. Client
#    → Uses the Target interface.
#    → Does not directly depend on the Adaptee.
#
# ============================================================
# WHY USE ADAPTER?
# ============================================================
#
# - Integrate third-party libraries.
# - Integrate legacy code.
# - Handle incompatible interfaces.
# - Avoid modifying existing/third-party classes.
# - Reduce coupling between client and external systems.
#
# ============================================================
# OCP CONNECTION
# ============================================================
#
# Without Adapter:
#
#     NotificationService → Twilio
#
# New provider may require modifying NotificationService.
#
# With Adapter:
#
#     NotificationService
#          ↑
#     TwilioAdapter → Twilio
#
#     NewProviderAdapter → NewProvider
#
# New provider → add a new Adapter instead of modifying
# existing client logic.
#
# Therefore, Adapter can help support the
# Open/Closed Principle.
#
# ============================================================
# ADAPTER vs DECORATOR
# ============================================================
#
# Adapter:
#     Changes/TRANSLATES the interface.
#
#     Old interface → Adapter → Expected interface
#
# Decorator:
#     Keeps the same interface and ADDS behavior.
#
#     Object → Decorator → More behavior
#
# EASY MEMORY:
#
# Adapter    → CHANGE interface
# Decorator  → ADD behavior
#
# ============================================================
# ADAPTER vs STRATEGY
# ============================================================
#
# Adapter:
#     Makes an existing incompatible class work.
#
# Strategy:
#     Provides interchangeable ways of performing a behavior.
#
# Adapter:
#     Twilio → TwilioAdapter → NotificationService
#
# Strategy:
#     Payment → UPI / Card / Wallet
#
# ============================================================
# WHEN TO THINK ADAPTER?
# ============================================================
#
# Look for:
# - Existing class has the wrong interface.
# - Third-party API doesn't match your interface.
# - Legacy code needs to work with new code.
# - Cannot/shouldn't modify the existing class.
#
# Common examples:
# - Third-party payment APIs
# - Notification providers
# - Legacy systems
# - External APIs
# - Database drivers
# - Cloud provider SDKs
#
# ============================================================
# INTERVIEW ONE-LINER
# ============================================================
#
# "Adapter Pattern converts the interface of an existing class
# into the interface expected by the client, allowing
# incompatible classes to work together."
#
# ============================================================

from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass


class Twilio:
    def send_sms(self, phone_number, message):
        print(f"Sending SMS to {phone_number}: {message}")

class Gmail:
    def send_mail(self, gmail_id,  message):
        print(f"Sending Gmail to {gmail_id}: {message}")


class TwilioAdapter(NotificationService):
    def __init__(self, notification_service, phone_number):
        self.phone_number = phone_number
        self.notification_service = notification_service

    def send(self, message):
        self.notification_service.send_sms(self.phone_number, message)


class GmailAdapter(NotificationService):
    def __init__(self, gmail, gmail_id):
        self.gmail = gmail
        self.gmail_id = gmail_id

    def send(self, message):
        self.gmail.send_mail(self.gmail_id, message)


def main():
    twilio = TwilioAdapter(Twilio(), 9764337401)
    twilio.send("Test description")

    print("==================================================================")
    gmail = GmailAdapter(Gmail(), "piyushnksingh@remedoapp.com")
    gmail.send("Test description")


if __name__ == "__main__":
    main()