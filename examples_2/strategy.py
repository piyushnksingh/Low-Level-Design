from abc import  ABC, abstractmethod

from solid_principles.DIP import MongoDBDatabase


class INotification(ABC):
    @abstractmethod
    def send_notification(self, msg: str):
        pass


class EmailNotification(INotification):
    def send_notification(self, msg: str):
        print(f"Email Notification: {msg}")

class SMSNotification(INotification):
    def send_notification(self, msg: str):
        print(f"SMS Notification: {msg}")

class PushNotification(INotification):
    def send_notification(self, msg: str):
        print(f"Push Notification: {msg}")


class NotificationStrategy:
    def __init__(self, strategy: INotification):
        self._strategy = strategy

    def set_strategy(self, strategy: INotification):
        self._strategy = strategy

    def notify(self, msg: str):
        self._strategy.send_notification(msg)

if __name__ == '__main__':
    message = "Hello World!"
    strategy = NotificationStrategy(EmailNotification())
    strategy. notify(message)

    strategy.set_strategy(SMSNotification())
    strategy.notify(message)

    strategy.set_strategy(PushNotification())
    strategy.notify(message)
