# ============================================================
# FACADE PATTERN
# ============================================================
#
# Definition:
# Facade Pattern provides a SIMPLE INTERFACE over a COMPLEX
# SUBSYSTEM.
#
# In simple words:
# Facade = SIMPLIFIED ENTRY POINT
#
# ============================================================
# CORE IDEA
# ============================================================
#
# Instead of the client directly interacting with multiple
# services, the Facade coordinates them behind one method.
#
# Without Facade:
#
# Client
#  ├── PaymentService
#  ├── InventoryService
#  ├── ShippingService
#  └── NotificationService
#
# With Facade:
#
# Client
#    ↓
# OrderFacade
#    ↓
# ├── PaymentService
# ├── InventoryService
# ├── ShippingService
# └── NotificationService
#
# Client only calls:
#
#     order_facade.place_order()
#
# ============================================================
# KEY COMPONENTS
# ============================================================
#
# 1. Facade
#    → Provides the simple interface.
#    → Coordinates subsystem operations.
#
# 2. Subsystems
#    → Existing services/classes that perform actual work.
#
# 3. Client
#    → Uses the Facade instead of directly interacting with
#      all subsystem classes.
#
# ============================================================
# WHY USE FACADE?
# ============================================================
#
# - Reduce client-side complexity.
# - Hide internal subsystem details.
# - Reduce direct dependencies from client to subsystems.
# - Provide a clean entry point to a complex operation.
# - Make the system easier for clients to use.
#
# ============================================================
# IMPORTANT
# ============================================================
#
# Facade does NOT necessarily remove or merge the subsystems.
#
# The underlying services still exist independently.
#
# Facade simply provides a convenient layer to coordinate them.
#
# ============================================================
# EXAMPLE
# ============================================================
#
# Order placement:
#
#     place_order()
#          ↓
#     Process Payment
#          ↓
#     Reserve Inventory
#          ↓
#     Create Shipment
#          ↓
#     Send Notification
#
# Client doesn't need to know these internal steps.
#
# ============================================================
# FACADE vs ADAPTER
# ============================================================
#
# Adapter:
#     Makes INCOMPATIBLE INTERFACES compatible.
#
#     Client → Adapter → Third-party/Legacy class
#
# Facade:
#     SIMPLIFIES a complex subsystem.
#
#     Client → Facade → Multiple subsystem classes
#
# EASY MEMORY:
#
# Adapter → CHANGE interface
# Facade  → SIMPLIFY interface
#
# ============================================================
# FACADE vs DECORATOR
# ============================================================
#
# Facade:
#     Hides complexity behind a simple interface.
#
# Decorator:
#     Adds behavior to an existing object.
#
# ============================================================
# WHEN TO THINK FACADE?
# ============================================================
#
# Look for:
# - Client needs to call many services for one operation.
# - Complex subsystem should be hidden.
# - Want one simple entry point.
# - Client has too many dependencies.
#
# Common examples:
# - Order processing
# - Payment checkout
# - User registration
# - Video processing
# - Cloud deployment workflows
# - Complex API/service orchestration
#
# ============================================================
# INTERVIEW ONE-LINER
# ============================================================
#
# "Facade provides a simplified interface over a complex
# subsystem, hiding its internal complexity and reducing the
# client's direct interaction with multiple components."
#
# ============================================================

class PaymentService:
    def process_payment(self, amount):
        print(f"Payment processed: ₹{amount}")


class InventoryService:
    def reserve_item(self, product_id):
        print(f"Inventory reserved for: {product_id}")


class ShippingService:
    def create_shipment(self, product_id):
        print(f"Shipment created for: {product_id}")


class NotificationService:
    def send_confirmation(self, product_id):
        print(f"Confirmation sent for: {product_id}")


class OrderFacade:
    def __init__(self):
        self.payment_service = PaymentService()
        self.inventory_service = InventoryService()
        self.shipping_service = ShippingService()
        self.notification_service = NotificationService()

    def place_order(self, product_id: str, amount: float ):
        self.payment_service.process_payment(amount)
        self.inventory_service.reserve_item(product_id)
        self.shipping_service.create_shipment(product_id)
        self.notification_service.send_confirmation(product_id)

def main():
    order = OrderFacade()
    order.place_order("P101", 999)


if __name__ == "__main__":
    main()