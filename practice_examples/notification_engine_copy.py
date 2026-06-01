from abc import ABC, abstractmethod
from typing import List


class INotification(ABC):
    @abstractmethod
    def get_content(self):
        pass


class SimpleNotification(INotification):
    def __init__(self, text: str):
        self._text = text

    def get_content(self) -> str:
        return self._text


class INotificationDecorator(INotification):
    def __init__(self, notification: INotification):
        self._notification = notification


class TimeStampDecorator(INotificationDecorator):
    def get_content(self) -> str:
        return "[2026-04-13 14:22:00] " + self._notification.get_content()


class SignatureDecorator(INotificationDecorator):
    def __init__(self, notification: INotification, signature: str):
        super().__init__(notification)
        self._signature = signature

    def get_content(self) -> str:
        return self._notification.get_content() + f"\n-- {self._signature}\n\n"
    

class IObserver(ABC):
    @abstractmethod
    def update(self):
        pass


class IObservable(ABC):
    @abstractmethod
    def add_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def remove_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self):
        pass


class NotificationObservable(IObservable):
    def __init__(self):
        self._observers: List[IObserver] = []
        self._latest_notification : INotification | None = None

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: IObserver):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

    def set_notification(self, notification: INotification):
        self._latest_notification = notification
        self.notify()

    def get_notification_content(self) -> INotification | str:
        return self._latest_notification.get_content() if self._latest_notification else ""


class Logger(IObserver):
    def __init__(self, observable: NotificationObservable):
        self._observable = observable

    def update(self):
        print("Logging New Notification:\n", self._observable.get_notification_content())


class INotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, content: str):
        pass


class SMSNotification(INotificationStrategy):
    def __init__(self, phone_number: int):
        self._phone_number = phone_number

    def send_notification(self, content: str):
        print(f"Sending SMS to {self._phone_number}\n{content}")


class EmailNotification(INotificationStrategy):
    def __init__(self, email: str):
        self._email_id = email

    def send_notification(self, content: str):
        print(f"Sending Email to {self._email_id}\n{content}")


class PopUpNotification(INotificationStrategy):
    def send_notification(self, content: str):
        print("Sending Popup Notification:\n", content)


class NotificationEngine(IObserver):
    def __init__(self, observable: NotificationObservable):
        self._observable = observable
        self._strategies: List[INotificationStrategy] = []

    def add_notification_strategy(self, strategy: INotificationStrategy):
        self._strategies.append(strategy)

    def update(self):
        content = self._observable.get_notification_content()
        for strategy in self._strategies:
            strategy.send_notification(content)


class NotificationService:
    _instance = None

    def __init__(self):
        if NotificationService._instance is not None:
            raise Exception("Use get_instance() instead")
        self._notifications: List[INotification] = []
        self._observable = NotificationObservable()

    @staticmethod
    def get_instance():
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance

    def send_notification(self, notification: INotification):
        self._notifications.append(notification)
        self._observable.set_notification(notification)

    def get_observable(self) -> NotificationObservable:
        return self._observable


def main():
    service = NotificationService().get_instance()
    observable = service.get_observable()

    logger = Logger(observable)
    engine = NotificationEngine(observable)

    engine.add_notification_strategy(SMSNotification(1533445563))
    engine.add_notification_strategy(EmailNotification("piyush@123.com"))
    engine.add_notification_strategy(PopUpNotification())

    observable.add_observer(engine)
    observable.add_observer(logger)

    notification = SimpleNotification("Your order has been shipped!")
    notification = TimeStampDecorator(notification)
    notification = SignatureDecorator(notification, "Customer care !!")

    service.send_notification(notification)

if __name__ == "__main__":
    main()