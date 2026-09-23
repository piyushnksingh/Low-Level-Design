# CHAIN OF RESPONSIBILITY DESIGN PATTERN
#
# Definition:
# Pass a request through a chain of handlers until the request
# is handled, partially handled, or cannot be handled further.
#
# Purpose:
# Pass a request through a chain of handlers.
# Each handler decides whether to handle the request
# or pass it to the next handler.
#
# Main benefit:
# Decouples the sender of a request from the object
# that handles the request.
#
# Components:
#
# 1. Handler
#    Defines common handling interface.
#    Maintains reference to next handler.
#
# 2. ConcreteHandler
#    Performs its specific responsibility.
#    If it cannot completely handle the request,
#    forwards it to the next handler.
#
# 3. Client
#    Creates handlers, builds the chain,
#    and sends the request to the first handler.
#
# Example:
#
# ATM withdrawal:
#
# Request
#    ↓
# ₹1000 Handler
#    ↓
# ₹500 Handler
#    ↓
# ₹200 Handler
#    ↓
# ₹100 Handler
#
# Each handler:
#
# Can handle?
#    ↓
# YES → handle request
#    ↓
# remaining?
#    ↓
# pass to next handler
#
# Common use cases:
# - Middleware
# - Authentication/Authorization pipelines
# - Logging pipelines
# - Validation pipelines
# - Approval workflows
# - ATM cash dispensing
#
# Key interview point:
# The sender doesn't need to know which handler
# will ultimately process the request.

from abc import ABC, abstractmethod

class MoneyHandler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next_handler(self, next_handler):
        self.next_handler = next_handler

    @abstractmethod
    def dispense(self, amount):
        pass


class ThousandHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 1000
        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹1000 notes.")

        remaining_amount = amount - (notes_needed * 1000)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled."
                )

class FiveHundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 500
        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹500 notes.")

        remaining_amount = amount - (notes_needed * 500)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled."
                )

class TwoHundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 200
        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹200 notes.")

        remaining_amount = amount - (notes_needed * 200)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled."
                )

class HundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 100
        if notes_needed > self.num_notes:
            notes_needed = self.num_notes
            self.num_notes = 0
        else:
            self.num_notes -= notes_needed

        if notes_needed > 0:
            print(f"Dispensing {notes_needed} x ₹100 notes.")

        remaining_amount = amount - (notes_needed * 100)

        if remaining_amount > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled."
                )


def main():
    thousand_handler = ThousandHandler(3)
    five_hundred_handler = FiveHundredHandler(5)
    two_hundred_handler = TwoHundredHandler(2)
    hundred_handler = HundredHandler(1)

    thousand_handler.set_next_handler(five_hundred_handler)
    five_hundred_handler.set_next_handler(two_hundred_handler)
    two_hundred_handler.set_next_handler(hundred_handler)

    amount = 1400

    print(f"Dispensing amount: {amount}")

    thousand_handler.dispense(amount)


# if __name__ == "__main__":
#     main()


# ------------------------------ OPTIMIZED CODE -----------------------------------------------
class MoneyHandler:

    def __init__(self, denomination, num_notes):
        self.denomination = denomination
        self.num_notes = num_notes
        self.next_handler = None

    def set_next_handler(self, next_handler):
        self.next_handler = next_handler

    def dispense(self, amount):

        notes_needed = min(
            amount // self.denomination,
            self.num_notes
        )

        self.num_notes -= notes_needed

        if notes_needed > 0:
            print(
                f"Dispensing {notes_needed} "
                f"x ₹{self.denomination} notes."
            )

        remaining_amount = (
            amount - notes_needed * self.denomination
        )

        if remaining_amount > 0:

            if self.next_handler:
                self.next_handler.dispense(remaining_amount)
            else:
                print(
                    f"Remaining amount of ₹{remaining_amount} "
                    "cannot be fulfilled."
                )


def main():

    thousand = MoneyHandler(1000, 3)
    five_hundred = MoneyHandler(500, 5)
    two_hundred = MoneyHandler(200, 10)
    hundred = MoneyHandler(100, 20)

    thousand.set_next_handler(five_hundred)
    five_hundred.set_next_handler(two_hundred)
    two_hundred.set_next_handler(hundred)

    amount = 4000
    print(f"Dispensing amount: {amount}")

    thousand.dispense(amount)


if __name__ == "__main__":
    main()