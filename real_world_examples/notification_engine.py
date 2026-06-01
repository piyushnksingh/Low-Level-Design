from abc import ABC, abstractmethod
from typing import List


class INotification(ABC):
    @abstractmethod
    def get_content(self):
        pass


class SimpleNotification(INotification):
    def __init__(self, text: str):
        self._text = text

    def get_content(self):
        return self._text


class INotificationDecorator(INotification):
    def __init__(self, notification: INotification):
        self._notification = notification


class TimeStampDecorator(INotificationDecorator):
    def get_content(self):
        return "[2026-04-13 14:22:00] " + self._notification.get_content()

class SignatureDecorator(INotificationDecorator):
    def __init__(self, notification: INotification, signature: str):
        super().__init__(notification)
        self._signature = signature

    def get_content(self):
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
    def notify_observer(self):
        pass


class NotificationObservable(IObservable):
    def __init__(self):
        self._observers: List[IObserver] = []
        self._current_notification: INotification | None = None

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: IObserver):
        self._observers.remove(observer)

    def notify_observer(self):
        for observer in self._observers:
            observer.update()

    def set_notification(self, notification: INotification):
        self._current_notification = notification
        self.notify_observer()

    def get_notification_content(self):
        return self._current_notification.get_content() if self._current_notification else ""


class Logger(IObserver):
    def __init__(self, observable: NotificationObservable):
        self._observable = observable

    def update(self):
        print("Logging New Notification:\n", self._observable.get_notification_content())


class INotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, content: str):
        pass


class EmailStrategy(INotificationStrategy):
    def __init__(self, email_id: str):
        self._email_id = email_id

    def send_notification(self, content: str):
        print(f"Sending Email to {self._email_id}\n{content}")

class SMSStrategy(INotificationStrategy):
    def __init__(self, phone_number: str):
        self._phone_number = phone_number

    def send_notification(self, content: str):
        print(f"Sending SMS to {self._phone_number}\n{content}")

class PopUpStrategy(INotificationStrategy):
    def send_notification(self, content: str):
        print("Sending Popup Notification:\n", content)


class NotificationEngine(IObserver):
    def __init__(self, observable: NotificationObservable):
        self._observable = observable
        self._strategies: List[INotificationStrategy] = [] # to support more than one notifications for a user

    def add_notification_strategy(self, strategy: INotificationStrategy):
        self._strategies.append(strategy)

    def update(self):
        content = self._observable.get_notification_content()
        for strategy in self._strategies:
            strategy.send_notification(content)


class NotificationService:
    _instance = None

    def __init__(self):
        self._observable = NotificationObservable()
        self._notifications: List[INotification] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NotificationService()
        return cls._instance

    def get_observable(self) -> NotificationObservable:
        return self._observable

    def send_notification(self, notification: INotification):
        self._notifications.append(notification)
        self._observable.set_notification(notification)

if __name__ == "__main__":
    service = NotificationService.get_instance()
    observable = service.get_observable()

    # Observers
    logger = Logger(observable)
    engine = NotificationEngine(observable)

    engine.add_notification_strategy(EmailStrategy("random.person@gmail.com"))
    engine.add_notification_strategy(SMSStrategy("+91 9876543210"))
    engine.add_notification_strategy(PopUpStrategy())

    observable.add_observer(logger)
    observable.add_observer(engine)

    # Create notification with decorators
    notification = SimpleNotification("Your order has been shipped!")
    notification = TimeStampDecorator(notification)
    notification = SignatureDecorator(notification, "Customer Care")

    service.send_notification(notification)
