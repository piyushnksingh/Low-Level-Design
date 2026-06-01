from abc import ABC, abstractmethod


# ===================== PAYMENT STRATEGY =====================

class PaymentStrategy(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


# ------------------ Concrete Strategies ---------------------

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def validate(self) -> bool:
        print("Validating Credit Card...")
        return len(self.card_number) == 16 and len(self.cvv) == 3

    def pay(self, amount: float) -> None:
        if not self.validate():
            raise Exception("Credit Card validation failed")
        print(f"Paid ₹{amount} using Credit Card")


class UPIPayment(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def validate(self) -> bool:
        print("Validating UPI ID & OTP...")
        return "@" in self.upi_id  # dummy validation

    def pay(self, amount: float) -> None:
        if not self.validate():
            raise Exception("UPI validation failed")
        print(f"Paid ₹{amount} using UPI")


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def validate(self) -> bool:
        print("Validating PayPal account...")
        return "@" in self.email

    def pay(self, amount: float) -> None:
        if not self.validate():
            raise Exception("PayPal validation failed")
        print(f"Paid ₹{amount} using PayPal")


# ===================== DISCOUNT STRATEGY =====================

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        return amount


class FestivalDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        print("Applying Festival Discount (10%)")
        return amount * 0.9


class PremiumUserDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        print("Applying Premium User Discount (20%)")
        return amount * 0.8


# ===================== CONTEXT =====================

class PaymentProcessor:
    def __init__(self,
                 payment_strategy: PaymentStrategy,
                 discount_strategy: DiscountStrategy = NoDiscount()):
        self.payment_strategy = payment_strategy
        self.discount_strategy = discount_strategy

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

    def set_discount_strategy(self, strategy: DiscountStrategy):
        self.discount_strategy = strategy

    def process_payment(self, amount: float):
        final_amount = self.discount_strategy.apply(amount)
        print(f"Final amount after discount: ₹{final_amount}")
        self.payment_strategy.pay(final_amount)


# ===================== CLIENT =====================

if __name__ == "__main__":
    # Payment method
    card_payment = CreditCardPayment("1234567812345678", "123")

    # Discount
    discount = FestivalDiscount()

    processor = PaymentProcessor(card_payment, discount)
    processor.process_payment(1000)

    print("\n--- Switching Strategy at Runtime ---\n")

    # Switch to UPI dynamically
    upi_payment = UPIPayment("user@upi")
    processor.set_payment_strategy(upi_payment)

    # Switch discount too
    processor.set_discount_strategy(PremiumUserDiscount())

    processor.process_payment(2000)