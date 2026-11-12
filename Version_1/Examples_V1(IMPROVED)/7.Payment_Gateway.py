import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self


# ============================
# Payment Request
# ============================
class PaymentRequest:
    def __init__(self, sender, receiver, amount, currency):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.currency = currency


# ============================
# Banking System
# Strategy Pattern
# ============================ 
class BankingSystem(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class PaytmBankingSystem(BankingSystem):
    def process_payment(self, amount):
        # Simulate 80% success
        print(f"Processing payment through Paytm of amount: {amount}")
        return random.randint(0, 99) < 80

class RazorPayBankingSystem(BankingSystem):
    def process_payment(self, amount):
        print(f"Processing payment through RazorPay of amount: {amount}")
        return random.randint(0, 99) < 90


# ============================
# Payment Gateway
# Template Method Pattern
# ============================
class PaymentGateway(ABC):
    def __init__(self):
        self.banking_system = None

    @abstractmethod
    def validate_payment(self, request):
        pass

    @abstractmethod
    def initiate_payment(self, request):
        pass

    @abstractmethod
    def confirm_payment(self, request):
        pass

    def process_payment(self, request):
        # Template method defining the standard payment flow.
        if not self.validate_payment(request):
            print(f"[PaymentGateway] Validation failed for {request.sender}")
            return False

        if not self.initiate_payment(request):
            print(f"[PaymentGateway] Initialization failed for {request.sender}")
            return False

        if not self.confirm_payment(request):
            print(f"[PaymentGateway] Confirmation failed for {request.sender}")
            return False

        return True


class PaytmPaymentGateway(PaymentGateway):
    def __init__(self):
        super().__init__()
        self.banking_system = PaytmBankingSystem()

    def validate_payment(self, request):
        print(f"[Paytm] Validating payment for {request.sender}")
        if request.amount <= 0 or request.currency != "INR":
            return False
        return True

    def initiate_payment(self, request):
        print(f"[Paytm] Initializing payment for {request.sender}")
        return self.banking_system.process_payment(request.amount)

    def confirm_payment(self, request):
        print(f"[Paytm] Confirming payment for {request.sender}")
        return True # Confirmation always succeeds in this simulation


class RazorPayPaymentGateway(PaymentGateway):
    def __init__(self):
        super().__init__()
        self.banking_system = RazorPayBankingSystem()

    def validate_payment(self, request):
        print(f"[RazorPay] Validating payment for {request.sender}")
        if request.amount <= 0 or request.currency != "INR":
            return False
        return True

    def initiate_payment(self, request):
        print(f"[RazorPay] Initializing payment for {request.sender}")
        return self.banking_system.process_payment(request.amount)

    def confirm_payment(self, request):
        print(f"[RazorPay] Confirming payment for {request.sender}")
        return True  # Confirmation always succeeds in this simulation


# ============================
# Payment Gateway Proxy
# Proxy Pattern
# ============================
class PaymentGatewayProxy(PaymentGateway):
    def __init__(self, gateway, max_retries):
        super().__init__()
        self.real_gateway = gateway
        self.max_retries = max_retries

    def process_payment(self, request):
        result = False
        for attempt in range(self.max_retries):
            if attempt > 0:
                print(f"[Proxy] Retrying payment (attempt {attempt + 1}) for {request.sender}.")

            result = self.real_gateway.process_payment(request)
            if result:
                break

        if not result:
            print(f"[Proxy] Payment failed after {self.max_retries} attempts for {request.sender}.")

        return result

    def validate_payment(self, request):
        return self.real_gateway.validate_payment(request)

    def initiate_payment(self, request):
        return self.real_gateway.initiate_payment(request)

    def confirm_payment(self, request):
        return self.real_gateway.confirm_payment(request)

# ============================
# Gateway Type
# ============================
class GatewayType(Enum):
    PAYTM = 1
    RAZORPAY = 2

# ============================
# Gateway Factory
# Factory + Singleton Pattern
# ============================
class GatewayFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            GatewayFactory._instance = super().__new__(cls)
        return GatewayFactory._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def get_gateway(self, gateway_type: GatewayType):
        if gateway_type == GatewayType.PAYTM:
            paytm_gateway = PaytmPaymentGateway()
            return PaymentGatewayProxy(paytm_gateway, 3)
        elif gateway_type == GatewayType.RAZORPAY:
            razorpay_gateway = RazorPayPaymentGateway()
            return PaymentGatewayProxy(razorpay_gateway, 1)
        else:
            raise ValueError("Unsupported gateway type")

# ============================
# Payment Service
# Singleton Pattern
# ============================
class PaymentService:
    _instance = None

    def __new__(cls):
        if PaymentService._instance is None:
            PaymentService._instance = super().__new__(cls)
            cls._instance.gateway = None
        return PaymentService._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def set_gateway(self, gateway):
        self.gateway = gateway

    def process_payment(self, request):
        if self.gateway is None:
            print("[PayentService] No gateway selected")
            return False
        return self.gateway.process_payment(request)

# ============================
# Payment Controller
# Singleton Pattern
# ============================
class PaymentController:
    _instance = None

    def __new__(cls):
        if PaymentController._instance is None:
            PaymentController._instance = super().__new__(cls)
        return PaymentController._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def handle_payment(self, gateway_type, request):
        payment_gateway = GatewayFactory.get_instance().get_gateway(gateway_type)
        payment_service = PaymentService.get_instance()
        payment_service.set_gateway(payment_gateway)
        return payment_service.process_payment(request)

def main():
    random.seed()

    request1 = PaymentRequest("Aditya", "Shubham", 1000, "INR")
    print("Processing via Paytm")
    print("------------------------------")
    result1 = PaymentController.get_instance().handle_payment(GatewayType.PAYTM, request1)
    print(f"Result: {'SUCCESS' if result1 else 'FAIL'}")

    request2 = PaymentRequest("Shubham", "Aditya", 500.0, "USD")
    print("Processing via RazorPay")
    print("------------------------------")
    result2 = PaymentController.get_instance().handle_payment(GatewayType.RAZORPAY, request2)
    print(f"Result: {'SUCCESS' if result2 else 'FAIL'}")

    print("---------------------------------")

if __name__ == "__main__":
    main()