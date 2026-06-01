from abc import ABC, abstractmethod

# ------------------ Target Interface ------------------
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


# ------------------ Adaptee 1 ------------------
class RazorpayAPI:
    def make_payment(self, amount_in_paise: int) -> None:
        print(f"Paid {amount_in_paise} paise using Razorpay")


# ------------------ Adapter 1 ------------------
class RazorpayAdapter(PaymentProcessor):
    def __init__(self, razorpay_api: RazorpayAPI):
        self.razorpay_api = razorpay_api

    def pay(self, amount: float) -> None:
        amount_in_paise = round(amount * 100)
        self.razorpay_api.make_payment(amount_in_paise)


# ------------------ Adaptee 2 ------------------
class StripeAPI:
    def charge(self, amount_in_dollars: float) -> None:
        print(f"Charged ${amount_in_dollars:.2f} using Stripe")


# ------------------ Adapter 2 ------------------
class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_api: StripeAPI, usd_rate: float):
        self.stripe_api = stripe_api
        self.usd_rate = usd_rate  # INR → USD conversion

    def pay(self, amount: float) -> None:
        amount_in_dollars = round(amount / self.usd_rate, 2)
        self.stripe_api.charge(amount_in_dollars)


# ------------------ Client ------------------
if __name__ == "__main__":
    processors = [
        RazorpayAdapter(RazorpayAPI()),
        StripeAdapter(StripeAPI(), usd_rate=83)
    ]

    for processor in processors:
        processor.pay(1000.75)