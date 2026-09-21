from abc import ABC, abstractmethod


# ABSTRACTION:
# Show WHAT an object can do, while hiding HOW it does it.
#
# Here, every payment method must implement pay(amount).
# The client does not need to know the internal payment logic.


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class UPIPayment(Payment):
    def pay(self, amount):
        print(f"Processing ₹{amount} through UPI")


class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Processing ₹{amount} through Credit Card")


class WalletPayment(Payment):
    def pay(self, amount):
        print(f"Processing ₹{amount} through Wallet")


# process_payment() is NOT required for abstraction.
#
# We keep it when there is common logic for all payment methods,
# such as validation, saving transactions, sending notifications, etc.
#
# It depends on the Payment abstraction, not a specific payment type.
# Therefore, adding a new payment method does not require changing
# this function.
def process_payment(payment: Payment, amount):
    if amount <= 0:
        raise ValueError("Invalid amount")

    payment.pay(amount)

    print("Saving transaction...")
    print("Sending notification...")


def main():
    process_payment(UPIPayment(), 1000)
    process_payment(CreditCardPayment(), 2000)
    process_payment(WalletPayment(), 500)


if __name__ == "__main__":
    main()


# INTERVIEW NOTES:
#
# Abstraction:
#   Defines WHAT an object should do, not HOW it does it.
#
# Payment -> defines the common contract: pay(amount)
# UPI/CreditCard/Wallet -> provide their own implementation.
#
# Adding a new payment method:
#   Create a new class implementing Payment.
#   Existing process_payment() logic remains unchanged.
#
# Abstraction vs Encapsulation:
#
# Abstraction:
#   Hides implementation complexity.
#   Example: payment.pay() hides internal payment steps.
#
# Encapsulation:
#   Protects and controls access to object data.
#   Example: BankAccount hides __balance and modifies it only
#   through deposit() and withdraw().
#
# IMPORTANT:
#   Program against abstractions, not concrete classes.
#
#   Good: process_payment(payment: Payment)
#   Less flexible: process_payment(payment: UPIPayment)
#
# Abstract class can have:
#   1. Abstract methods -> subclasses must implement them.
#   2. Concrete methods -> common logic shared by subclasses.