from abc import ABC, abstractmethod

class INotification(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass

class SimpleNotification(INotification):
    def __init__(self, msg: str):
        self._text = msg

    def get_content(self) -> str:
        return self._text

class INotificationDecorator(INotification):
    def __init__(self, notification: INotification):
        self._notification = notification

    def get_content(self) -> str:
        return self._notification.get_content()

class TimestampDecorator(INotificationDecorator):
    def __init__(self, notification: INotification):
        super().__init__(notification)

    def get_content(self) -> str:
        content = self._notification.get_content()
        return "[2025-09-01 14:00:01] " + content

class SignatureDecorator(INotificationDecorator):
    def __init__(self, notification: INotification, signature: str):
        super().__init__(notification)
        self._signature = signature

    def get_content(self) -> str:
        content = self._notification.get_content()
        return content + " with Signature: " + self._signature


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
    def notify_observers(self):
        pass


class NotificationObservable(IObservable):
    def __init__(self):
        self._observers = []
        self._current_notification = None

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: IObserver):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

    def set_notification(self, notification: INotification):
        self._current_notification = notification
        self.notify_observers()

    def get_notification(self) -> INotification:
        return self._current_notification

    def get_notification_content(self) -> str:
        if self._current_notification is None:
            return ""
        return self._current_notification.get_content()

class Logger(IObserver):
    def __init__(self, observable=None):
        if observable is None:
            observable = NotificationService.get_instance().get_observable()

        self.notification_observable = observable
        self.notification_observable.add_observer(self)

    def update(self):
        print("Logging New Notification: \n"
              + self.notification_observable.get_notification_content())

class INotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, content: str):
        pass

class EmailStrategy(INotificationStrategy):
    def __init__(self, email_id: str):
        self.email_id = email_id

    def send_notification(self, content: str):
        print(f"Sending Email Notification to: {self.email_id} " + content)

class SMSStrategy(INotificationStrategy):
    def __init__(self, mobile_number: str):
        self.mobile_number = mobile_number

    def send_notification(self, content: str):
        print(f"Sending SMS Notification to: {self.mobile_number} " + content)

class PopUpStrategy(INotificationStrategy):
    def send_notification(self, content: str):
        print(f"Sending Popup Notification: " + content)


class NotificationEngine(IObserver):
    def __init__(self, observable=None):
        if observable is None:
            observable = NotificationService.get_instance().get_observable()

        self.notification_observable = observable
        self.notification_strategies = []
        # Register in both cases
        self.notification_observable.add_observer(self)

    def add_notification_strategy(self, strategy: INotificationStrategy):
        self.notification_strategies.append(strategy)

    def remove_notification_strategy(self, strategy: INotificationStrategy):
        self.notification_strategies.remove(strategy)

    def update(self):
        content = self.notification_observable.get_notification_content()
        for strategy in self.notification_strategies:
            strategy.send_notification(content)

class NotificationService:
    _instance = None

    def __init__(self):
        if NotificationService._instance is not None:
            raise Exception("Use get_instance() instead...")
        self.observable = NotificationObservable()
        self.notifications = []

    @staticmethod
    def get_instance():
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance

    def get_observable(self) -> NotificationObservable:
        return self.observable

    def send_notification(self, notification: INotification):
        self.notifications.append(notification)
        self.observable.set_notification(notification)

def main():
    notification_service = NotificationService.get_instance()

    notification_observable = notification_service.get_observable()

    logger = Logger(notification_observable)

    notification_engine = NotificationEngine(notification_observable)

    # Add Notification Strategies
    notification_engine.add_notification_strategy(
        EmailStrategy("random.person@gmail.com"))

    notification_engine.add_notification_strategy(
        SMSStrategy("+91 9876543210"))

    notification_engine.add_notification_strategy(
        PopUpStrategy())

    # notification_observable.add_observer(logger)
    # notification_observable.add_observer(notification_engine)

    notification = SimpleNotification("Your Order has been Shipped !")

    notification = TimestampDecorator(notification)

    notification = SignatureDecorator(notification, "Customer Care")

    notification_observable.set_notification(notification)

if __name__ == "__main__":
    main()
