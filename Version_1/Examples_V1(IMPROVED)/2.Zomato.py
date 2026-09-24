from abc import ABC, abstractmethod
from typing import List, Optional


# ============================================================
# MENU ITEM
# ============================================================
class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    def get_code(self) -> str:
        return self._code

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> int:
        return self._price

    def set_price(self, price: int):
        self._price = price

# ============================================================
# RESTAURANT
# ============================================================
class Restaurant:
    _id = 0
    def __init__(self, restaurant_name: str, location: str):
        Restaurant._id += 1
        self._id = Restaurant._id
        self._name = restaurant_name
        self._location = location
        self._menu_items: List[MenuItem] = []

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_location(self) -> str:
        return self._location

    def get_menu_items(self) -> List[MenuItem]:
        return self._menu_items

    def add_menu_item(self, item: MenuItem):
        self._menu_items.append(item)

# ============================================================
# RESTAURANT MANAGER
# ============================================================
class RestaurantManager:
    def __init__(self):
        self._restaurants: List[Restaurant] = []

    def add_restaurant(self, restaurant: Restaurant):
        if restaurant not in self._restaurants:
            self._restaurants.append(restaurant)

    def remove_restaurant(self, restaurant: Restaurant):
        if restaurant in self._restaurants:
            self._restaurants.remove(restaurant)

    def get_restaurants_by_location(self, location: str) -> List[Restaurant]:
        return [restaurant for restaurant in self._restaurants if restaurant.get_location() == location]

# ============================================================
# CART
# ============================================================
class Cart:
    def __init__(self):
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []

    def set_restaurant(self, restaurant: Restaurant):
        self._restaurant = restaurant
        self._items.clear()

    def get_restaurant(self) -> Optional[Restaurant]:
        return self._restaurant

    def add_item(self, item: MenuItem):
        if self._restaurant is None:
            raise ValueError("Please select a restaurant before adding items.")

        if item not in self._items:
            self._items.append(item)

    def remove_item(self, item: MenuItem):
        if item in self._items:
            self._items.remove(item)

    def get_items(self) -> List[MenuItem]:
        return self._items

    def get_total_cost(self) -> float:
        return sum(item.get_price() for item in self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def clear(self):
        self._items.clear()
        self._restaurant = None

# ============================================================
# USER
# ============================================================
class User:
    _id = 0
    def __init__(self, name: str, email: str, address: str):
        User._id += 1
        self._id = User._id
        self._name = name
        self._email = email
        self._address = address
        self._cart = Cart()

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_email(self) -> str:
        return self._email

    def get_address(self) -> str:
        return self._address

    def get_cart(self) -> Cart:
        return self._cart

# ============================================================
# PAYMENT STRATEGY
# ============================================================
class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class UPIPayment(IPaymentStrategy):
    def __init__(self, phone_number: str):
        self._phone_number = phone_number

    def pay(self, amount: float):
        print(f"Paying ₹{amount} through UPI using {self._phone_number}")

class CreditCardPayment(IPaymentStrategy):
    def __init__(self, card_details: str):
        self._card_details = card_details

    def pay(self, amount: float):
        print(f"Paying ₹{amount} through Credit Card using {self._card_details}")

class NetBankingPayment(IPaymentStrategy):
    def __init__(self, net_banking_details: str):
        self._net_banking_details = net_banking_details

    def pay(self, amount: float):
        print(f"Paying ₹{amount} through Net Banking using {self._net_banking_details}")

# ============================================================
# ORDER
# ============================================================
class Order:
    _id = 0

    def __init__(self):
        Order._id += 1
        self._id = Order._id
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []
        self._user: Optional[User] = None
        self._payment_strategy: Optional[IPaymentStrategy] = None

    def get_order_id(self) -> int:
        return self._id

    def set_user(self, user: User):
        self._user = user

    def get_user(self) -> User:
        return self._user

    def set_restaurant(self, restaurant: Restaurant):
        self._restaurant = restaurant

    def get_restaurant(self) -> Restaurant:
        return self._restaurant

    def set_items(self, items: List[MenuItem]):
        self._items = list(items)

    def get_items(self) -> List[MenuItem]:
        return self._items

    def set_payment_strategy(self, strategy: IPaymentStrategy):
        self._payment_strategy = strategy

    def get_total(self) -> float:
        return sum(item.get_price() for item in self._items)

    def process_payment(self) -> bool:
        if self._payment_strategy is None:
            print("Please choose a payment mode first.")
            return False

        self._payment_strategy.pay(self.get_total())
        return True

    def get_type(self) -> str:
        return "Order"

# ============================================================
# DELIVERY ORDER
# ============================================================
class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self._user_address = ""

    def set_user_address(self, address: str):
        self._user_address = address

    def get_user_address(self) -> str:
        return self._user_address

    def get_type(self) -> str:
        return "Delivery"

# ============================================================
# PICKUP ORDER
# ============================================================
class PickUpOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurant_address = ""

    def set_restaurant_address(self, address: str):
        self._restaurant_address = address

    def get_restaurant_address(self) -> str:
        return self._restaurant_address

    def get_type(self) -> str:
        return "PickUp"

# ============================================================
# ORDER FACTORY
# ============================================================
class OrderFactory:
    @staticmethod
    def create_order(user: User, restaurant: Restaurant, menu_items: List[MenuItem], payment_strategy: IPaymentStrategy,
        order_type: str) -> Order:

        if order_type == "Delivery":
            order = DeliveryOrder()
            order.set_user_address(user.get_address())
        elif order_type == "PickUp":
            order = PickUpOrder()
            order.set_restaurant_address(restaurant.get_location())
        else:
            raise ValueError(f"Invalid order type: {order_type}")

        order.set_user(user)
        order.set_restaurant(restaurant)
        order.set_items(menu_items)
        order.set_payment_strategy(payment_strategy)
        return order
# ============================================================
# ORDER MANAGER
# ============================================================

class OrderManager:
    def __init__(self):
        self._orders = {}

    def add_order(self, order: Order):
        self._orders[order.get_order_id()] = order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._orders.get(order_id)

    def get_orders_by_user(self, user: User) -> List[Order]:
        return [order for order in self._orders.values() if order.get_user() == user]

    def list_orders(self):
        print("\n========== ALL ORDERS ==========")

        for order in self._orders.values():
            print(
                f"Order ID: {order.get_order_id()} | "
                f"Type: {order.get_type()} | "
                f"User: {order.get_user().get_name()} | "
                f"Restaurant: {order.get_restaurant().get_name()} | "
                f"Total: ₹{order.get_total()}"
            )


# ============================================================
# CART SERVICE
# ============================================================

class CartService:
    def select_restaurant(self, user: User, restaurant: Restaurant):
        user.get_cart().set_restaurant(restaurant)

    def add_item(self, user: User, item_code: str):
        cart = user.get_cart()
        restaurant = cart.get_restaurant()

        if restaurant is None:
            raise ValueError("Please select a restaurant first.")

        for item in restaurant.get_menu_items():
            if item.get_code() == item_code:
                cart.add_item(item)
                return

        raise ValueError(f"Item {item_code} not found.")

    def remove_item(self, user: User, item_code: str):
        cart = user.get_cart()

        for item in cart.get_items():
            if item.get_code() == item_code:
                cart.remove_item(item)
                return

        raise ValueError(f"Item {item_code} not found in cart.")

    def print_cart(self, user: User):
        cart = user.get_cart()

        print("\n========== CART ==========")

        if cart.is_empty():
            print("Cart is empty.")
            return

        print(f"Restaurant: {cart.get_restaurant().get_name()}")

        print("\nItems:")

        for item in cart.get_items():
            print(
                f"{item.get_code()} | "
                f"{item.get_name()} | "
                f"₹{item.get_price()}"
            )

        print(f"\nGrand Total: ₹{cart.get_total_cost()}")


# ============================================================
# NOTIFICATION SERVICE
# ============================================================

class NotificationService:
    def notify(self, order: Order):
        print("\n========== NOTIFICATION ==========")

        print(f"New {order.get_type()} order placed!")

        print(f"Order ID: {order.get_order_id()}")

        print(
            f"Customer: "
            f"{order.get_user().get_name()}"
        )

        print(
            f"Restaurant: "
            f"{order.get_restaurant().get_name()}"
        )

        print("\nItems:")

        for item in order.get_items():
            print(
                f" - {item.get_name()} "
                f"(₹{item.get_price()})"
            )

        print(f"\nTotal: ₹{order.get_total()}")

        print("Payment: Done")


# ============================================================
# ORDER SERVICE
# ============================================================

class OrderService:
    def __init__(
        self,
        order_manager: OrderManager,
        order_factory: OrderFactory,
        notification_service: NotificationService
    ):
        self._order_manager = order_manager
        self._order_factory = order_factory
        self._notification_service = notification_service

    def checkout(
        self,
        user: User,
        order_type: str,
        payment_strategy: IPaymentStrategy
    ) -> Order:

        cart = user.get_cart()

        if cart.is_empty():
            raise ValueError("Cannot checkout with an empty cart.")

        restaurant = cart.get_restaurant()

        order = self._order_factory.create_order(
            user=user,
            restaurant=restaurant,
            menu_items=cart.get_items(),
            payment_strategy=payment_strategy,
            order_type=order_type
        )

        self._order_manager.add_order(order)

        return order

    def pay_for_order(
        self,
        user: User,
        order: Order
    ) -> bool:

        payment_successful = order.process_payment()

        if not payment_successful:
            return False

        self._notification_service.notify(order)

        user.get_cart().clear()

        return True


# ============================================================
# TOMATO APPLICATION
# ============================================================

class Tomato:
    def __init__(self):

        # Managers
        self._restaurant_manager = RestaurantManager()
        self._order_manager = OrderManager()

        # Services
        self._cart_service = CartService()
        self._notification_service = NotificationService()

        # Factory
        self._order_factory = OrderFactory()

        # Order workflow
        self._order_service = OrderService(
            self._order_manager,
            self._order_factory,
            self._notification_service
        )

        self._initialize_restaurants()

    def _initialize_restaurants(self):
        restaurant1 = Restaurant(
            "Bikaner",
            "Delhi"
        )

        restaurant1.add_menu_item(
            MenuItem(
                "P1",
                "Chole Bhature",
                120
            )
        )

        restaurant1.add_menu_item(
            MenuItem(
                "P2",
                "Samosa",
                15
            )
        )

        restaurant2 = Restaurant(
            "Haldiram",
            "Kolkata"
        )

        restaurant2.add_menu_item(
            MenuItem(
                "P1",
                "Raj Kachori",
                80
            )
        )

        restaurant2.add_menu_item(
            MenuItem(
                "P2",
                "Pav Bhaji",
                100
            )
        )

        restaurant2.add_menu_item(
            MenuItem(
                "P3",
                "Dhokla",
                50
            )
        )

        restaurant3 = Restaurant(
            "Saravana Bhavan",
            "Chennai"
        )

        restaurant3.add_menu_item(
            MenuItem(
                "P1",
                "Masala Dosa",
                90
            )
        )

        restaurant3.add_menu_item(
            MenuItem(
                "P2",
                "Idli Vada",
                60
            )
        )

        restaurant3.add_menu_item(
            MenuItem(
                "P3",
                "Filter Coffee",
                30
            )
        )

        self._restaurant_manager.add_restaurant(restaurant1)
        self._restaurant_manager.add_restaurant(restaurant2)
        self._restaurant_manager.add_restaurant(restaurant3)

    # --------------------------------------------------------
    # Restaurant operations
    # --------------------------------------------------------

    def search_restaurants(self, location: str) -> List[Restaurant]:
        return self._restaurant_manager.get_restaurants_by_location(location)

    # --------------------------------------------------------
    # Cart operations
    # --------------------------------------------------------

    def select_restaurant(
        self,
        user: User,
        restaurant: Restaurant
    ):
        self._cart_service.select_restaurant(user, restaurant)

    def add_to_cart(
        self,
        user: User,
        item_code: str
    ):
        self._cart_service.add_item(user, item_code)

    def print_cart(self, user: User):
        self._cart_service.print_cart(user)

    # --------------------------------------------------------
    # Order operations
    # --------------------------------------------------------

    def checkout(
        self,
        user: User,
        order_type: str,
        payment_strategy: IPaymentStrategy
    ) -> Order:

        return self._order_service.checkout(
            user,
            order_type,
            payment_strategy
        )

    def pay_for_order(
        self,
        user: User,
        order: Order
    ):
        return self._order_service.pay_for_order(user, order)


# ============================================================
# MAIN
# ============================================================

def main():
    # Create application
    tomato = Tomato()

    # Create user
    user = User(
        name="Piyush",
        email="piyush@123.com",
        address="Hyderabad"
    )

    print(f"User: {user.get_name()} is active.")

    # --------------------------------------------------------
    # 1. Search restaurants
    # --------------------------------------------------------

    restaurant_list = tomato.search_restaurants("Delhi")

    if not restaurant_list:
        print("No restaurants found!")
        return

    print("\n========== RESTAURANTS ==========")

    for restaurant in restaurant_list:
        print(
            f"{restaurant.get_name()} - "
            f"{restaurant.get_location()}"
        )

    # --------------------------------------------------------
    # 2. Select restaurant
    # --------------------------------------------------------

    restaurant = restaurant_list[0]

    tomato.select_restaurant(
        user,
        restaurant
    )

    print(
        f"\nSelected restaurant: "
        f"{restaurant.get_name()}"
    )

    # --------------------------------------------------------
    # 3. Add items to cart
    # --------------------------------------------------------

    tomato.add_to_cart(user, "P1")
    tomato.add_to_cart(user, "P2")

    # --------------------------------------------------------
    # 4. Print cart
    # --------------------------------------------------------

    tomato.print_cart(user)

    # --------------------------------------------------------
    # 5. Checkout
    # --------------------------------------------------------

    order = tomato.checkout(
        user=user,
        order_type="Delivery",
        payment_strategy=UPIPayment("9139143356")
    )

    print("\nOrder created successfully!")

    print(f"Order ID: {order.get_order_id()}")

    # --------------------------------------------------------
    # 6. Pay
    # --------------------------------------------------------

    tomato.pay_for_order(
        user,
        order
    )

    # --------------------------------------------------------
    # 7. Verify OrderManager
    # --------------------------------------------------------

    print("\n========== ORDER MANAGER ==========")

    saved_order = tomato._order_manager.get_order(
        order.get_order_id()
    )

    print(
        f"Retrieved Order ID: "
        f"{saved_order.get_order_id()}"
    )

    print(
        f"Order Type: "
        f"{saved_order.get_type()}"
    )

    print(
        f"Total: "
        f"₹{saved_order.get_total()}"
    )


if __name__ == "__main__":
    main()