class PaymentService:
    @staticmethod
    def pay(amount: float):
        print(f"Payment of ₹{amount} processed successfully")


class InventoryService:
    @staticmethod
    def reserve_product(product: str, quantity: int):
        print(f"Reserved {quantity} unit(s) of {product}")


class ShippingService:
    @staticmethod
    def create_shipment(address: str):
        print(f"Shipment created for address: {address}")


class NotificationService:
    @staticmethod
    def notify(message: str):
        print(f"Notification sent: {message}")


# Facade
class CheckoutFacade:

    def __init__(
        self,
        payment_service: PaymentService,
        inventory_service: InventoryService,
        shipping_service: ShippingService,
        notification_service: NotificationService
    ):
        self._payment_service = payment_service
        self._inventory_service = inventory_service
        self._shipping_service = shipping_service
        self._notification_service = notification_service

    def place_order(
        self,
        product: str,
        quantity: int,
        amount: float,
        address: str
    ):

        try:
            # Step 1: Reserve Inventory
            self._inventory_service.reserve_product(product, quantity)

            # Step 2: Process Payment
            self._payment_service.pay(amount)

            # Step 3: Create Shipment
            self._shipping_service.create_shipment(address)

            # Step 4: Notify User
            self._notification_service.notify(
                f"Order placed successfully for {product}"
            )

            print("Order completed successfully")

        except Exception as e:
            print(f"Order failed: {e}")


# Client Code
if __name__ == "__main__":

    # Subsystems
    payment_service = PaymentService()
    inventory_service = InventoryService()
    shipping_service = ShippingService()
    notification_service = NotificationService()

    # Facade
    checkout = CheckoutFacade(
        payment_service,
        inventory_service,
        shipping_service,
        notification_service
    )

    # Client interacts only with facade
    checkout.place_order(
        product="iPhone 16",
        quantity=1,
        amount=79999,
        address="Mumbai, India"
    )