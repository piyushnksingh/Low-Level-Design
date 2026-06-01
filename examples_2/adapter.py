from abc import ABC, abstractmethod

class EmailNotificationProvider:
    def send_email(self, payload: str):
        print("Send email with message: {}".format(payload))

class SMSNotificationProvider:
    def send_sms(self, payload: str):
        print("Send sms with message: {}".format(payload))

class PushNotificationProvider:
    def trigger_push_notification(self, payload: str):
        print("Trigger push notification: {}".format(payload))

class INotification(ABC):
    @abstractmethod
    def send_notification(self, notification):
        pass

class EmailAdapter(INotification):
    def __init__(self, provider: EmailNotificationProvider):
        self._provider = provider

    def send_notification(self, payload: str):
        self._provider.send_email(payload)


class SMSAdapter(INotification):
    def __init__(self, provider: SMSNotificationProvider):
        self._provider = provider

    def send_notification(self, payload: str):
        self._provider.send_sms(payload)


class PushAdapter(INotification):
    def __init__(self, provider: PushNotificationProvider):
        self._provider = provider

    def send_notification(self, payload: str):
        self._provider.trigger_push_notification(payload)

class NotificationService:
    def __init__(self, adapter: INotification):
        self._adapter = adapter

    def notify(self, msg: str):
        self._adapter.send_notification(msg)


if __name__ == "__main__":
    message = "Hello World!"

    # Email Notification
    email_service = NotificationService(
        EmailAdapter(EmailNotificationProvider())
    )
    email_service.notify(message)

    print()

    # SMS Notification
    sms_service = NotificationService(
        SMSAdapter(SMSNotificationProvider())
    )
    sms_service.notify(message)

    print()

    # Push Notification
    push_service = NotificationService(
        PushAdapter(PushNotificationProvider())
    )
    push_service.notify(message)

