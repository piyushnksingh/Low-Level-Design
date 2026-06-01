# DEFINITION : OPEN TO EXTENSION BUT, CLOSE TO MODIFICATION
from abc import ABC, abstractmethod


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return self.products

    def calculate_total(self):
        return sum(p.price for p in self.products)


# Printer (SRP ✅)
class ShoppingCartPrinter:
    def __init__(self, cart):
        self.cart = cart

    def print_invoice(self):
        print("Shopping Cart Invoice:")
        for p in self.cart.get_products():
            print(f"{p.name} - Rs {p.price}")
        print(f"Total: Rs {self.cart.calculate_total()}")


# Storage Strategy (OCP ✅)
class StorageStrategy(ABC):
    @abstractmethod
    def save(self, cart):
        pass


class SQLStorage(StorageStrategy):
    def save(self, cart):
        print("Saving shopping cart to SQL DB...")


class MongoStorage(StorageStrategy):
    def save(self, cart):
        print("Saving shopping cart to Mongo DB...")


class FileStorage(StorageStrategy):
    def save(self, cart):
        print("Saving shopping cart to File...")


# Context class
class ShoppingCartStorage:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def save(self, cart):
        self.strategy.save(cart)


# Driver
if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_product(Product("Laptop", 50000))
    cart.add_product(Product("Mouse", 2000))

    printer = ShoppingCartPrinter(cart)
    printer.print_invoice()

    storage = ShoppingCartStorage(SQLStorage())
    storage.save(cart)