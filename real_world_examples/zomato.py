from abc import abstractmethod, ABC
from typing import List


# -------------------------------- MODELS ------------------------------
class MenuItem:
    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    # Getters
    def get_code(self) -> str:
        return self._code

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> int:
        return self._price

    # Setters
    def set_code(self, code: str):
        self._code = code

    def set_name(self, name: str):
        self._name = name

    def set_price(self, price: int):
        self._price = price


class Restaurant:
    _id = 0
    def __init__(self, restaurant_name: str, location: str):
        Restaurant._id += 1
        self.restaurant_id = Restaurant._id
        self.name = restaurant_name
        self.menu_items : List[MenuItem] = []
        self.location = location

    # Getters
    def get_name(self) -> str:
        return self.name

    def get_location(self) -> str:
        return self.location

    def get_menu(self):
        return self.menu_items  # returns list (like vector reference)

    # Setters
    def set_name(self, name: str):
        self.name = name

    def set_location(self, location: str):
        self.location = location

    # Business logic
    def add_menu_item(self, item):
        self.menu_items.append(item)


class Cart:
    def __init__(self):
        self._restaurant = None  # reference to Restaurant
        self._items = []  # list of MenuItem

    def add_item(self, item):
        if not self._restaurant:
            print("Cart: Set a restaurant before adding items.")
            return
        self._items.append(item)

    def get_total_cost(self) -> float:
        return sum(item.get_price() for item in self._items)

    def is_empty(self) -> bool:
        return (self._restaurant is None) or (len(self._items) == 0)

    def clear(self):
        self._items.clear()
        self._restaurant = None

    # Getters and Setters
    def set_restaurant(self, restaurant):
        self._restaurant = restaurant

    def get_restaurant(self):
        return self._restaurant

    def get_items(self):
        return self._items


class User:
    _id = 0
    def __init__(self, name: str, address: str):
        User._id += 1
        self.user_id = User._id
        self._name = name
        self._address = address
        self._cart = Cart()  # no pointer, direct object

    # Getters
    def get_name(self) -> str:
        return self._name

    def get_address(self) -> str:
        return self._address

    def get_cart(self):
        return self._cart

    # Setters
    def set_name(self, name: str):
        self._name = name

    def set_address(self, address: str):
        self._address = address


class Order(ABC):
    _next_order_id = 0  # static variable

    def __init__(self):
        Order._next_order_id += 1
        self._order_id = Order._next_order_id
        self._user = None
        self._restaurant = None
        self._items = []
        self._payment_strategy = None
        self._total = 0.0

    def process_payment(self) -> bool:
        if self._payment_strategy:
            self._payment_strategy.pay(self._total)
            return True
        else:
            print("Please choose a payment mode first")
            return False

    @abstractmethod
    def get_type(self) -> str:
        pass

    # Getters / Setters
    def get_order_id(self) -> int:
        return self._order_id

    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user

    def set_restaurant(self, restaurant):
        self._restaurant = restaurant

    def get_restaurant(self):
        return self._restaurant

    def set_items(self, items):
        self._items = items
        self._total = sum(item.get_price() for item in items)

    def get_items(self):
        return self._items

    def set_payment_strategy(self, strategy):
        self._payment_strategy = strategy

    def get_total(self) -> float:
        return self._total

    def set_total(self, total: float):
        self._total = total


class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self._user_address = ""

    def get_type(self):
        return "Delivery"

    # Getters / Setters
    def set_user_address(self, address: str):
        self._user_address = address

    def get_user_address(self) -> str:
        return self._user_address


class PickupOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurant_address = ""

    def get_type(self) -> str:
        return "Pickup"

    # Getters / Setters
    def set_restaurant_address(self, address: str):
        self._restaurant_address = address

    def get_restaurant_address(self) -> str:
        return self._restaurant_address



# ---------------------------- SINGLETON and MANAGERS -------------------------------
class RestaurantManager:
    _instance = None
    def __init__(self):
        if RestaurantManager._instance is not None:
            raise Exception("Use get_instance() instead")
        self.restaurants : List[Restaurant] = []

    @staticmethod
    def get_instance():
        if RestaurantManager._instance is None:
            RestaurantManager._instance = RestaurantManager()
        return RestaurantManager._instance

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)

    def search_restaurant_by_location(self, location: str) -> List[Restaurant]:
        return [restaurant for restaurant in self.restaurants
                if restaurant.location == location]


class OrderManager:
    _instance = None
    def __init__(self):
        if OrderManager._instance is not None:
            raise Exception("Use get_instance() instead")
        self._orders: List[Order] = []

    @staticmethod
    def get_instance():
        if OrderManager._instance is None:
            OrderManager._instance = OrderManager()
        return OrderManager._instance

    def add_order(self, order: Order):
        self._orders.append(order)

    def list_orders(self):
        print("\n--- All Orders ---")
        for order in self._orders:
            print(
                f"{order.get_type()} order for {order.get_user().get_name()} "
                f"| Total: ₹{order.get_total()} "
            )


# ---------------------------- STRATEGY ----------------------------------------------
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: str):
        pass


class UPIPaymentStrategy(PaymentStrategy):
    def pay(self, amount: str):
        print("Paying through UPI...")


class CreditCardPaymentStrategy(PaymentStrategy):
    def pay(self, amount: str):
        print("Paying through Credit Card...")


# -------------------------------- FACTORY ------------------------------------------
class OrderFactory(ABC):
    @abstractmethod
    def create_order(self, user, cart, restaurant, menu_items,
        payment_strategy, total_cost: float, order_type: str):
        pass


class NowOrderFactory(OrderFactory):
    def create_order(self, user, cart, restaurant, menu_items, payment_strategy, total_cost, order_type):
        order = None

        if order_type == "Delivery":
            delivery_order = DeliveryOrder()
            delivery_order.set_user_address(user.get_address())
            order = delivery_order
        else:
            pickup_order = PickupOrder()
            pickup_order.set_restaurant_address(restaurant.get_location())
            order = pickup_order

        order.set_user(user)
        order.set_restaurant(restaurant)
        order.set_items(menu_items)
        order.set_payment_strategy(payment_strategy)
        order.set_total(total_cost)

        return order


class ScheduleOrderFactory(OrderFactory):
    def create_order(self, user, cart, restaurant, menu_items, payment_strategy, total_cost, order_type):
        order = None

        if order_type == "Delivery":
            delivery_order = DeliveryOrder()
            delivery_order.set_user_address(user.get_address())
            order = delivery_order
        else:
            pickup_order = PickupOrder()
            pickup_order.set_restaurant_address(restaurant.get_location())
            order = pickup_order

        order.set_user(user)
        order.set_restaurant(restaurant)
        order.set_items(menu_items)
        order.set_payment_strategy(payment_strategy)
        order.set_total(total_cost)

        return order


# ------------------------------ services --------------------------
class NotificationService:

    @staticmethod
    def notify(order):
        print(f"\nNotification: New {order.get_type()} order placed!")
        print("---------------------------------------------")
        print(f"Order ID: {order.get_order_id()}")
        print(f"Customer: {order.get_user().get_name()}")
        print(f"Restaurant: {order.get_restaurant().get_name()}")
        print("Items Ordered:")

        for item in order.get_items():
            print(f"   - {item.get_name()} (₹{item.get_price()})")

        print(f"Total: ₹{order.get_total()}")
        print("Payment: Done")
        print("---------------------------------------------")

# --------------------------------- ZOMATO ----------------------------------------
class TomatoApp:
    def __init__(self):
        self.initialize_restaurants()

    def initialize_restaurants(self):
        restaurant1 = Restaurant("Bikaner", "Delhi")
        restaurant1.add_menu_item(MenuItem("P1", "Chole Bhature", 120))
        restaurant1.add_menu_item(MenuItem("P2", "Samosa", 15))

        restaurant2 = Restaurant("Haldiram", "Kolkata")
        restaurant2.add_menu_item(MenuItem("P1", "Raj Kachori", 80))
        restaurant2.add_menu_item(MenuItem("P2", "Pav Bhaji", 100))
        restaurant2.add_menu_item(MenuItem("P3", "Dhokla", 50))

        restaurant3 = Restaurant("Saravana Bhavan", "Chennai")
        restaurant3.add_menu_item(MenuItem("P1", "Masala Dosa", 90))
        restaurant3.add_menu_item(MenuItem("P2", "Idli Vada", 60))
        restaurant3.add_menu_item(MenuItem("P3", "Filter Coffee", 30))

        manager = RestaurantManager.get_instance()
        manager.add_restaurant(restaurant1)
        manager.add_restaurant(restaurant2)
        manager.add_restaurant(restaurant3)

    def search_restaurants(self, location: str):
        return RestaurantManager.get_instance().search_restaurant_by_location(location)

    def select_restaurant(self, user, restaurant):
        user.get_cart().set_restaurant(restaurant)

    def add_to_cart(self, user, item_code: str):
        cart = user.get_cart()
        restaurant = cart.get_restaurant()

        if not restaurant:
            print("Please select a restaurant first.")
            return

        for item in restaurant.get_menu():
            if item.get_code() == item_code:
                cart.add_item(item)
                break

    def checkout_now(self, user, order_type, payment_strategy):
        return self.checkout(user, order_type, payment_strategy, NowOrderFactory())

    def checkout_scheduled(self, user, order_type, payment_strategy):
        return self.checkout(user, order_type, payment_strategy, ScheduleOrderFactory)

    def checkout(self, user, order_type, payment_strategy, order_factory):
        cart = user.get_cart()

        if cart.is_empty():
            return None

        restaurant = cart.get_restaurant()
        items = cart.get_items()
        total_cost = cart.get_total_cost()

        order = order_factory.create_order(
            user, cart, restaurant, items,
            payment_strategy, total_cost, order_type
        )

        OrderManager.get_instance().add_order(order)
        return order

    def pay_for_order(self, user, order):
        is_payment_success = order.process_payment()

        if is_payment_success:
            notification = NotificationService()
            notification.notify(order)
            user.get_cart().clear()

    def print_user_cart(self, user):
        cart = user.get_cart()

        print("Items in cart:")
        print("------------------------------------")
        for item in cart.get_items():
            print(f"{item.get_code()} : {item.get_name()} : ₹{item.get_price()}")
        print("------------------------------------")
        print(f"Grand total : ₹{cart.get_total_cost()}")


def main():
    # Create TomatoApp Object
    tomato = TomatoApp()

    # Simulate a user coming in (Happy Flow)
    user = User("Aditya", "Delhi")
    print(f"User: {user.get_name()} is active.")

    # User searches for restaurants by location
    restaurant_list = tomato.search_restaurants("Delhi")

    if not restaurant_list:
        print("No restaurants found!")
        return

    print("Found Restaurants:")
    for restaurant in restaurant_list:
        print(f" - {restaurant.get_name()}")

    # User selects a restaurant
    tomato.select_restaurant(user, restaurant_list[0])
    print(f"Selected restaurant: {restaurant_list[0].get_name()}")

    # User adds items to the cart
    tomato.add_to_cart(user, "P1")
    tomato.add_to_cart(user, "P2")

    tomato.print_user_cart(user)

    # User checkout the cart
    order = tomato.checkout_now(
        user,
        "Delivery",
        UPIPaymentStrategy()
    )

    # User pays for the order
    tomato.pay_for_order(user, order)


if __name__ == "__main__":
    main()


