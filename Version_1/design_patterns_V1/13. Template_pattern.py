
from abc import ABC, abstractmethod
from typing import final


class PaymentGateway(ABC):

    def __init__(self, amount: float):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        self._amount = amount

    @final
    def process_payment(self):
        try:
            self.before_payment()
            self.validate_payment()
            self.initiate_payment()
            self.confirm_payment()
            self.after_payment()
            self.success_message()

        except Exception as e:
            self.failure_message(str(e))
            raise

    @abstractmethod
    def validate_payment(self):
        pass

    @abstractmethod
    def initiate_payment(self):
        pass

    @abstractmethod
    def confirm_payment(self):
        pass

    def success_message(self):
        print(f"Payment successful: Rs. {self._amount}")

    def failure_message(self, reason):
        print(f"Payment failed: {reason}")

    def before_payment(self):
        """Optional hook"""
        pass

    def after_payment(self):
        """Optional hook"""
        pass


class RazorPay(PaymentGateway):

    def before_payment(self):
        print("[RazorPay] Starting payment process")

    def validate_payment(self):
        print("[RazorPay] Validating payment")

    def initiate_payment(self):
        print("[RazorPay] Initiating payment")

    def confirm_payment(self):
        print("[RazorPay] Confirming payment")

    def after_payment(self):
        print("[RazorPay] Payment process completed")


class Paytm(PaymentGateway):

    def validate_payment(self):
        print("[Paytm] Validating payment")

    def initiate_payment(self):
        print("[Paytm] Initiating payment")

    def confirm_payment(self):
        print("[Paytm] Confirming payment")


def main():
    razorpay = RazorPay(100)
    razorpay.process_payment()

    print()

    paytm = Paytm(200)
    paytm.process_payment()


if __name__ == "__main__":
    main()
