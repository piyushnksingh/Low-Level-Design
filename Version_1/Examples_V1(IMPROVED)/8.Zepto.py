from abc import abstractmethod, ABC
from math import sqrt


class Product:
    def __init__(self, sku: int, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

    def get_sku(self):
        return self.sku

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

class ProductFactory:
    @staticmethod
    def create_product(sku: int) -> Product:
        # In reality, product details would come from a database.
        products = {
            101: ("Apple", 20),
            102: ("Banana", 10),
            103: ("Chocolate", 50),
            201: ("T-Shirt", 500),
            202: ("Jeans", 1000),
        }

        name, price = products.get(sku, (f"Item_{sku}", 100))
        return Product(sku, name, price)

class InventoryStore(ABC):
    @abstractmethod
    def add_product(self, product: Product, qty: int):
        pass

    @abstractmethod
    def remove_product(self, sku: int, qty: int):
        pass

    @abstractmethod
    def check_stock(self, sku: int) -> int:
        pass

    @abstractmethod
    def list_available_products(self) -> list[Product]:
        pass

class DBInventoryStore(InventoryStore):
    def __init__(self):
        self.stock = {}          # SKU -> quantity
        self.products = {}       # SKU -> Product

    def add_product(self, product: Product, qty: int):
        sku = product.get_sku()
        if sku not in self.products:
            self.products[sku] = product
        self.stock[sku] = self.stock.get(sku, 0) + qty

    def remove_product(self, sku: int, qty: int):
        if sku not in self.stock:
            return

        current_quantity = self.stock[sku]
        remaining_quantity = current_quantity - qty

        if remaining_quantity > 0:
            self.stock[sku] = remaining_quantity
        else:
            self.stock.pop(sku)

    def check_stock(self, sku: int) -> int:
        return self.stock.get(sku, 0)

    def list_available_products(self) -> list[Product]:
        available_items = []
        for sku, qty in self.stock.items():
            if qty > 0 and sku in self.products:
                available_items.append(self.products[sku])

        return available_items

class InventoryManager:
    def __init__(self, store: InventoryStore):
        self.store = store

    def add_stock(self, sku: int, qty: int):
        product = ProductFactory.create_product(sku)
        self.store.add_product(product, qty)
        print(f"[InventoryManager] added SKU {sku} Qty {qty}")

    def remove_stock(self, sku: int, qty: int):
        self.store.remove_product(sku, qty)

    def check_stock(self, sku: int):
        return self.store.check_stock(sku)

    def get_available_product(self):
        return self.store.list_available_products()

class ReplenishStrategy(ABC):
    @abstractmethod
    def replenish(self, manager: InventoryManager, items_to_replenish: dict[int, int]):
        pass

class ThresholdReplenishStrategy(ReplenishStrategy):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def replenish(self, manager: InventoryManager, items_to_replenish: dict[int, int]):
        print("[ThresholdReplenish] Checking threshold...")
        for sku, qty_to_add in items_to_replenish.items():
            current_qty = manager.check_stock(sku)
            if current_qty < self.threshold:
                manager.add_stock(sku, qty_to_add)
                print(f"-> SKKU {sku} was {current_qty}, replenished by {qty_to_add}")


class WeeklyReplenishStrategy(ReplenishStrategy):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def replenish(self, manager: InventoryManager, items_to_replenish: dict[int, int]):
        print("[WeeklyReplenish] Weekly replenishment triggered for inventory.")

class DarkStore:
    def __init__(self, name: str, x_cord: float, y_cord: float):
        self.name = name
        self.x_cord = x_cord
        self.y_cord = y_cord

        self.inventory_manager = InventoryManager(DBInventoryStore())
        self.replenish_strategy = None

    def distance_to(self, ux: float, uy: float) -> float:
        return sqrt((self.x_cord - ux) ** 2 + (self.y_cord - uy) ** 2)

    def run_replenishment(self, items_to_replenish: dict[int, int]):
        if self.replenish_strategy:
            self.replenish_strategy.replenish(self.inventory_manager, items_to_replenish)

    # Delegation methods
    def get_all_product(self):
        return self.inventory_manager.get_available_product()

    def check_stock(self, sku: int) -> int:
        return self.inventory_manager.check_stock(sku)

    def remove_stock(self, sku: int, qty: int):
        self.inventory_manager.remove_stock(sku, qty)

    def add_stock(self, sku: int, qty: int):
        self.inventory_manager.add_stock(sku, qty)

    # Getters & Setters
    def set_replenish_strategy(self, strategy: ReplenishStrategy):
        self.replenish_strategy = strategy

    def get_name(self):
        return self.name

    def get_x_coordinate(self):
        return self.x_cord

    def get_y_coordinate(self):
        return self.y_cord

    def get_inventory_manager(self):
        return self.inventory_manager

class DarkStoreManager:
    _instance = None

    def __init__(self):
        self.darK_stores = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_dark_store(self, dark_store: DarkStore):
        self.darK_stores.append(dark_store)

    def get_nearby_store(self, x: float, y: float, max_distance: float) -> list[DarkStore]:
        distance_list = []
        for dark_store in self.darK_stores:
            distance = dark_store.distance_to(x, y)
            if distance <= max_distance:
                distance_list.append((distance, dark_store))

        distance_list.sort(key=lambda item: item[0])

        return [dark_store for distance, dark_store in distance_list]

class Cart:
    def __init__(self):
        self.items: list[tuple[Product, int]] = []           # Product -> Quantity

    def add_product(self, sku: int, qty: int):
        product = ProductFactory.create_product(sku)
        self.items.append((product, qty))
        print(f"[Cart] Added SKU {sku} ({product.get_name()}) x {qty}")

    def get_total(self) -> float:
        total = 0.0
        for product, qty in self.items:
            price = product.get_price()
            total += price * qty
        return total

    def get_items(self):
        return self.items

class User:
    def __init__(self, name: str, x_cord: float, y_cord: float):
        self.name = name
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.cart = Cart()

    def get_cart(self):
        return self.cart

class DeliveryPartner:
    def __init__(self, name: str):
        self.name = name

class Order:
    next_id = 1
    def __init__(self, user: User):
        self.order_id = Order.next_id
        Order.next_id += 1

        self.user = user
        self.items: list[tuple[Product, int]] = []
        self.partners: list[DeliveryPartner] = []
        self.total = 0.0

class OrderManager:
    _instance = None

    def __init__(self):
        self.orders: list[Order] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def place_order(self, user: User, cart: Cart):

        print(
            f"\n[OrderManager] Placing Order for: {user.name}"
        )

        requested_items = cart.get_items()

        # 1. Find nearby dark stores within 5 KM.

        max_distance = 5.0

        nearby_dark_stores = (
            DarkStoreManager
            .get_instance()
            .get_nearby_store(
                user.x_cord,
                user.y_cord,
                max_distance
            )
        )

        if not nearby_dark_stores:
            print(
                "  No dark stores within 5 KM. "
                "Cannot fulfill order."
            )

            return

        # 2. Check whether the closest store has all items.

        first_store = nearby_dark_stores[0]

        all_in_first = True

        for product, qty in requested_items:

            sku = product.get_sku()

            if first_store.check_stock(sku) < qty:
                all_in_first = False
                break

        order = Order(user)

        # ====================================================
        # Case 1: All items available in the closest store
        # ====================================================

        if all_in_first:

            print(
                f"  All items at: {first_store.get_name()}"
            )

            for product, qty in requested_items:
                sku = product.get_sku()

                first_store.remove_stock(sku, qty)

                order.items.append((product, qty))

            order.total = cart.get_total()

            order.partners.append(
                DeliveryPartner("Partner1")
            )

            print(
                "  Assigned Delivery Partner: Partner1"
            )

        # ====================================================
        # Case 2: Split order across multiple stores
        # ====================================================

        else:

            print(
                "  Splitting order across stores..."
            )

            # SKU -> Quantity required

            all_items = {}

            for product, qty in requested_items:
                sku = product.get_sku()

                all_items[sku] = (
                        all_items.get(sku, 0) + qty
                )

            partner_id = 1

            for store in nearby_dark_stores:

                # All SKUs have been assigned.

                if not all_items:
                    break

                print(
                    f"   Checking: {store.get_name()}"
                )

                assigned = False

                to_erase = []

                # Use a snapshot because quantities can change.

                for sku, qty_needed in list(
                        all_items.items()
                ):

                    available_qty = store.check_stock(sku)

                    if available_qty <= 0:
                        continue

                    # Take the smaller of available and required.

                    taken_qty = min(
                        available_qty,
                        qty_needed
                    )

                    store.remove_stock(sku, taken_qty)

                    print(
                        f"     {store.get_name()} supplies "
                        f"SKU {sku} x{taken_qty}"
                    )

                    order.items.append(
                        (
                            ProductFactory.create_product(sku),
                            taken_qty
                        )
                    )

                    # Adjust remaining quantity.

                    if qty_needed > taken_qty:

                        all_items[sku] = (
                                qty_needed - taken_qty
                        )

                    else:

                        to_erase.append(sku)

                    assigned = True

                # Remove fully satisfied SKUs.

                for sku in to_erase:
                    all_items.pop(sku, None)

                # Assign a partner if this store supplied items.

                if assigned:
                    partner_name = (
                        f"Partner{partner_id}"
                    )

                    partner_id += 1

                    order.partners.append(
                        DeliveryPartner(partner_name)
                    )

                    print(
                        f"     Assigned: {partner_name} "
                        f"for {store.get_name()}"
                    )

            # Print unfulfilled quantities.

            if all_items:

                print("  Could not fulfill:")

                for sku, qty in all_items.items():
                    print(
                        f"    SKU {sku} x{qty}"
                    )

            # Recalculate order total.

            total = 0.0

            for product, qty in order.items:
                total += (
                        product.get_price() * qty
                )

            order.total = total

        # ====================================================
        # Order Summary
        # ====================================================

        print(
            f"\n[OrderManager] Order "
            f"#{order.order_id} Summary:"
        )

        print(f"  User: {user.name}")

        print("  Items:")

        for product, qty in order.items:
            print(
                f"    SKU {product.get_sku()} "
                f"({product.get_name()}) x{qty} "
                f"@ ₹{product.get_price()}"
            )

        print(
            f"  Total: ₹{order.total}"
        )

        print("  Partners:")

        for partner in order.partners:
            print(f"    {partner.name}")

        print()

        self.orders.append(order)

    def get_all_orders(self) -> list[Order]:
        return self.orders


# ============================================================
# ZeptoHelper
# ============================================================

class ZeptoHelper:

    @staticmethod
    def show_all_items(user: User):

        print(
            f"\n[Zepto] All Available products within "
            f"5 KM for {user.name}:"
        )

        ds_manager = DarkStoreManager.get_instance()

        nearby_stores = (
            ds_manager.get_nearby_store(
                user.x_cord,
                user.y_cord,
                5.0
            )
        )

        # SKU -> Price
        sku_to_price = {}

        # SKU -> Name
        sku_to_name = {}

        for dark_store in nearby_stores:

            products = dark_store.get_all_product()

            for product in products:

                sku = product.get_sku()

                if sku not in sku_to_price:

                    sku_to_price[sku] = (
                        product.get_price()
                    )

                    sku_to_name[sku] = (
                        product.get_name()
                    )

        for sku, price in sku_to_price.items():

            print(
                f"  SKU {sku} - "
                f"{sku_to_name[sku]} @ ₹{price}"
            )

    @staticmethod
    def initialize():

        ds_manager = DarkStoreManager.get_instance()

        # ----------------------------------------------------
        # DarkStore A
        # ----------------------------------------------------

        dark_store_a = DarkStore(
            "DarkStoreA",
            0.0,
            0.0
        )

        dark_store_a.set_replenish_strategy(
            ThresholdReplenishStrategy(3)
        )

        print(
            "\nAdding stocks in DarkStoreA...."
        )

        dark_store_a.add_stock(101, 5)  # Apple
        dark_store_a.add_stock(102, 2)  # Banana

        # ----------------------------------------------------
        # DarkStore B
        # ----------------------------------------------------

        dark_store_b = DarkStore(
            "DarkStoreB",
            4.0,
            1.0
        )

        dark_store_b.set_replenish_strategy(
            ThresholdReplenishStrategy(3)
        )

        print(
            "\nAdding stocks in DarkStoreB...."
        )

        dark_store_b.add_stock(101, 3)   # Apple
        dark_store_b.add_stock(103, 10)   # Chocolate

        # ----------------------------------------------------
        # DarkStore C
        # ----------------------------------------------------

        dark_store_c = DarkStore(
            "DarkStoreC",
            2.0,
            3.0
        )

        dark_store_c.set_replenish_strategy(
            ThresholdReplenishStrategy(3)
        )

        print(
            "\nAdding stocks in DarkStoreC...."
        )

        dark_store_c.add_stock(102, 5)    # Banana
        dark_store_c.add_stock(201, 7)    # T-Shirt

        # Register dark stores.

        ds_manager.register_dark_store(
            dark_store_a
        )

        ds_manager.register_dark_store(
            dark_store_b
        )

        ds_manager.register_dark_store(
            dark_store_c
        )

def main():

    # 1. Initialize dark stores.

    ZeptoHelper.initialize()

    # 2. A user comes onto the platform.

    user = User(
        "Aditya",
        1.0,
        1.0
    )

    print(
        f"\nUser with name {user.name} "
        f"comes on platform"
    )

    # 3. Show all available products.

    ZeptoHelper.show_all_items(user)

    # 4. User adds items to cart.

    print(
        "\nAdding items to cart"
    )

    cart = user.get_cart()

    cart.add_product(101, 4)   # Apple
    cart.add_product(102, 3)   # Banana
    cart.add_product(103, 2)   # Chocolate

    # 5. Place order.

    OrderManager.get_instance().place_order(
        user,
        user.cart
    )


if __name__ == "__main__":
    main()

































