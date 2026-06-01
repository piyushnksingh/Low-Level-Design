from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class IObservable(ABC):
    @abstractmethod
    def add_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def remove_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, msg: str):
        pass


class Asset(IObservable):
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
        self._observers = []

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: IObserver):
        self._observers.remove(observer)

    def set_price(self, price: float):
        self._price = price
        self.notify(f"Price changed to {price} for {self._name} stock")

    def get_price(self):
        return self._price

    def notify(self, msg: str):
        for observer in self._observers:
            try:
                observer.update(msg)
            except Exception as e:
                print(f"Failed to notify observer: {e}")


class Stock(Asset):
    pass


class Gold(Asset):
    pass


class User(IObserver):
    def __init__(self, name: str):
        self._name = name

    def update(self, msg: str):
        print(f"Notification for {self._name} : {msg}")


if __name__ == "__main__":
    observable_1 = Stock("Reliance", 100.0)
    observable_2 = Gold("Reliance_Gold", 1000.0)
    observable_3 = Stock("JIO", 200.0)
    observable_4 = Gold("JIO_Gold", 2000.0)

    piyush = User("Piyush")

    observable_1.add_observer(piyush)
    observable_2.add_observer(piyush)

    prashant = User("Prashant")

    observable_1.add_observer(prashant)
    observable_2.add_observer(prashant)
    observable_3.add_observer(prashant)
    observable_4.add_observer(prashant)

    observable_1.set_price(300.0)
    observable_2.set_price(3000.0)
    observable_3.set_price(400.0)
    observable_4.set_price(4000.0)







