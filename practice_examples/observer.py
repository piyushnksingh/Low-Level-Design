from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, stock_name: str, price: float):
        pass

class Observable(ABC):
    @abstractmethod
    def add_observer(self, user: Observer):
        pass

    @abstractmethod
    def remove_observer(self, user: Observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass


class Stock(Observable):
    def __init__(self, stock_name: str, price: float):
        self._stock_name = stock_name
        self._price = price
        self._observers: List[Observer] = []

    def add_observer(self, user: Observer):
        self._observers.append(user)

    def remove_observer(self, user: Observer):
        self._observers.remove(user)

    def notify_observer(self):
        for observer in self._observers:
            observer.update(self._stock_name, self._price)

    def update_stock_price(self, price: float):
        self._price = price
        self.notify_observer()

    def get_stock_price(self) -> float:
        return self._price


class User(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, stock_name: str, price: float):
        print(f"[Notification] {self.name}: {stock_name} is now {price}")


if __name__ == "__main__":
    stock_1 = Stock("APPLE", 100)
    stock_2 = Stock("GOOGLE", 200)

    user_1 = User("prashant")
    user_2 = User("piyush")

    stock_1.add_observer(user_1)
    stock_2.add_observer(user_2)

    stock_1.add_observer(user_2)
    stock_2.add_observer(user_1)

    stock_1.update_stock_price(500)
    stock_2.update_stock_price(600)