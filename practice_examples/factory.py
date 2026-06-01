from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class Email(Notification):
    def __init__(self, email: str):
        self.email = email

    def send(self, message: str) -> None:
        print(f"message: {message} sent to email: {self.email}")

class SMS(Notification):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"message: {message} sent to phone number: {self.phone_number}")

class Push(Notification):
    def __init__(self, device_id: str):
        self.device_id = device_id

    def send(self, message: str) -> None:
        print(f"message: {message} sent to device_id: {self.device_id}")


class NotificationFactory:
    _registry = {}

    @classmethod
    def register(cls, key: str, creator):
        cls._registry[key] = creator

    @classmethod
    def create(cls, via: str, creds: str):
        if via not in cls._registry:
            raise ValueError(f"Unsupported notification type: {via}")
        return cls._registry[via](creds)



if __name__ == "__main__":
    notification_factory = NotificationFactory()
    NotificationFactory.register("email", Email)
    NotificationFactory.register("sms", SMS)
    NotificationFactory.register("push", Push)

    sms_notification = notification_factory.create("sms", "9999888877")
    sms_notification.send("Hello there! How are you?", )

    push_notification = notification_factory.create("push", "123456")
    push_notification.send("Hello there! How are you?", )

    notification = notification_factory.create("email", "")
    notification.send("Hello there! How are you?", )

