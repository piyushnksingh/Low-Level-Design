from abc import ABC, abstractmethod
from typing import List


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
        self._id = Restaurant._id
        self._name = restaurant_name
        self._location = location
        self._menu_items: List[MenuItem] = []

    def get_name(self):
        return self._name

    def get_location(self):
        return self._location

    def get_menu_items(self):
        return self._menu_items

    def set_name(self, name: str):
        self._name = name

    def set_location(self, location: str):
        self._location = location

    def add_menu_items(self, item: MenuItem):
        self._menu_items.append(item)

class RestaurantManager:
    _instance = None

    def __init__(self):
        if RestaurantManager._instance is not None:
            raise Exception("Use get_instance() instead")
        self._restaurants: List[Restaurant] = []

    @staticmethod
    def get_instance():
        if RestaurantManager._instance is None:
            RestaurantManager._instance = RestaurantManager()
        return RestaurantManager._instance

    def add_restaurant(self, restaurant: Restaurant):
        if restaurant not in self._restaurants:
            self._restaurants.append(restaurant)

    def remove_restaurant(self, restaurant: Restaurant):
        if restaurant in self._restaurants:
            self._restaurants.remove(restaurant)

    def get_restaurants_by_location(self, location: str) -> List[Restaurant]:
        restaurants = []
        for restaurant in self._restaurants:
            if restaurant.get_location() == location:
                restaurants.append(restaurant)

        return restaurants

class Cart:
    _id = 0
    def __init__(self):
        Cart._id += 1
        self._id = Cart._id
        self._restaurant = None
        self._items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        if self._restaurant is None:
            print("Cart: Set a restaurant before adding items.")
            return
        if item not in self._items:
            self._items.append(item)

    def remove_item(self, item: MenuItem):
        if item in self._items:
            self._items.remove(item)

    def get_total_cost(self):
        return sum(item.get_price() for item in self._items)

    def is_empty(self):
        return self._items == [] or self._restaurant is None

    def clear(self):
        self._items = []
        self._restaurant = None

    def set_restaurant(self, restaurant):
        self._restaurant = restaurant

    def get_restaurant(self):
        return self._restaurant

    def get_items(self):
        return self._items

class User:
    _id = 0
    def __init__(self, name: str, email: str, address: str):
        User._id += 1
        self._id = User._id
        self._name = name
        self._email = email
        self._address = address
        self._cart = Cart()

    def get_name(self) -> str:
        return self._name

    def get_address(self) -> str:
        return self._address

    def get_email(self) -> str:
        return self._email

    def get_cart(self):
        return self._cart

    def set_name(self, name: str):
        self._name = name

    def set_address(self, address: str):
        self._address = address

class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class UPIPayment(IPaymentStrategy):
    def __init__(self, phone_number: str):
        self._phone_number = phone_number

    def pay(self, amount: float):
        print(f"Paying amount {amount} through UPI Payment using {self._phone_number}")

class CreditCardPayment(IPaymentStrategy):
    def __init__(self, card_details: str):
        self._card_details = card_details

    def pay(self, amount: float):
        print(f"Paying amount {amount} through Credit Card Payment using {self._card_details}")

class NetBankingPayment(IPaymentStrategy):
    def __init__(self, net_banking_details: str):
        self._net_banking_details = net_banking_details

    def pay(self, amount: float):
        print(f"Paying amount {amount} through Net Banking Payment using {self._net_banking_details}")

class Order:
    _id = 0
    def __init__(self):
        Order._id += 1
        self._id = Order._id
        self._restaurant = None
        self._items = []
        self._user = None
        self._payment_strategy = None
        
    def process_payment(self) -> bool:
        amount = self.get_total()
        if self._payment_strategy: 
            self._payment_strategy.pay(amount)
            return True
        else:
            print("Please choose a payment mode first")
            return False

    def get_type(self):
        pass

    # Getters / Setters
    def get_order_id(self) -> int:
        return self._id

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

    def get_items(self):
        return self._items

    def set_payment_strategy(self, strategy):
        self._payment_strategy = strategy

    def get_total(self) -> float:
        return sum(item.get_price() for item in self._items)

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
        
class PickUpOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurant_address = ""

    def get_type(self):
        return "PickUp"

    # Getters / Setters
    def set_restaurant_address(self, address: str):
        self._restaurant_address = address

    def get_restaurant_address(self) -> str:
        return self._restaurant_address
    
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

class IOrderFactory(ABC):
    @abstractmethod
    def create_order(self, user: User, restaurant: Restaurant, menu_items: List[MenuItem],
        payment_strategy: IPaymentStrategy, order_type: str):
        pass

class NowOrderFactory(IOrderFactory):
    def create_order(self, user: User, restaurant: Restaurant, menu_items: List[MenuItem],
        payment_strategy: IPaymentStrategy, order_type: Order):

        if order_type == "Delivery":
            order = DeliveryOrder()
            order.set_user_address(user.get_address())
        else:
            order = PickUpOrder()
            order.set_restaurant_address(restaurant.get_location())

        order.set_payment_strategy(payment_strategy)
        order.set_user(user)
        order.set_items(menu_items)
        order.set_restaurant(restaurant)

        return order

class ScheduledOrderFactory(IOrderFactory):
    def create_order(self, user: User, restaurant: Restaurant,
                     menu_items: List[MenuItem],
                     payment_strategy: IPaymentStrategy, order_type: Order):

        if order_type == "Delivery":
            order = DeliveryOrder()
            order.set_user_address(user.get_address())
        else:
            order = PickUpOrder()
            order.set_restaurant_address(restaurant.get_location())

        order.set_payment_strategy(payment_strategy)
        order.set_user(user)
        order.set_items(menu_items)
        order.set_restaurant(restaurant)

        return order
    
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
        
class Tomato:
    def __init__(self):
        self._initialize_restaurants()
        
    @staticmethod
    def _initialize_restaurants():
        restaurant1 = Restaurant("Bikaner", "Delhi")
        restaurant1.add_menu_items(MenuItem("P1", "Chole Bhature", 120))
        restaurant1.add_menu_items(MenuItem("P2", "Samosa", 15))

        restaurant2 = Restaurant("Haldiram", "Kolkata")
        restaurant2.add_menu_items(MenuItem("P1", "Raj Kachori", 80))
        restaurant2.add_menu_items(MenuItem("P2", "Pav Bhaji", 100))
        restaurant2.add_menu_items(MenuItem("P3", "Dhokla", 50))

        restaurant3 = Restaurant("Saravana Bhavan", "Chennai")
        restaurant3.add_menu_items(MenuItem("P1", "Masala Dosa", 90))
        restaurant3.add_menu_items(MenuItem("P2", "Idli Vada", 60))
        restaurant3.add_menu_items(MenuItem("P3", "Filter Coffee", 30))

        manager = RestaurantManager.get_instance()
        manager.add_restaurant(restaurant1)
        manager.add_restaurant(restaurant2)
        manager.add_restaurant(restaurant3)
        
    @staticmethod
    def search_restaurants(location: str):
        return RestaurantManager.get_instance().get_restaurants_by_location(location)
    
    @staticmethod
    def select_restaurant(user: User, restaurant: Restaurant):
        user.get_cart().set_restaurant(restaurant)
        
    @staticmethod
    def add_to_cart(user: User, item_code: str):
        cart = user.get_cart()
        restaurant = cart.get_restaurant()
        for item in restaurant.get_menu_items():
            if item.get_code() == item_code:
                cart.add_item(item)
                break

    @staticmethod
    def checkout(user: User, order_type: str, payment_strategy: IPaymentStrategy, order_factory: IOrderFactory):
        cart = user.get_cart()
        if cart.is_empty():
            return None

        restaurant = cart.get_restaurant()
        items = cart.get_items()

        order = order_factory.create_order(
            user, restaurant, items, payment_strategy, order_type)

        OrderManager.get_instance().add_order(order)
        return order

    def checkout_now(self, user: User, order_type: str, payment_strategy: IPaymentStrategy):
        return self.checkout(user, order_type, payment_strategy, NowOrderFactory())

    def checkout_scheduled(self, user: User, order_type: str, payment_strategy: IPaymentStrategy):
        return self.checkout(user, order_type, payment_strategy, ScheduledOrderFactory())

    @staticmethod
    def pay_for_order(user: User, order: Order):
        payment_status = order.process_payment()

        if payment_status:
            notification = NotificationService()
            notification.notify(order)
            user.get_cart().clear()

    @staticmethod
    def print_user_cart(user):
        cart = user.get_cart()

        print("Items in cart:")
        print("------------------------------------")
        for item in cart.get_items():
            print(f"{item.get_code()} : {item.get_name()} : ₹{item.get_price()}")
        print("------------------------------------")
        print(f"Grand total : ₹{cart.get_total_cost()}")

def main():
    tomato = Tomato()

    user = User("piyush", "piyush@123.com", "Hyderabad")
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
    restaurant = restaurant_list[0]
    tomato.select_restaurant(user, restaurant)
    print(f"Selected restaurant: {restaurant.get_name()}")

    # User adds items to the cart
    tomato.add_to_cart(user, "P1")
    tomato.add_to_cart(user, "P2")

    tomato.print_user_cart(user)

    order = tomato.checkout_now(
        user, "Delivery", UPIPayment("9139143356"))

    tomato.pay_for_order(user, order)


if __name__ == "__main__":
    main()
    
        