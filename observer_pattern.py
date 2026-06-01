from abc import ABC, abstractmethod
from typing import List


# ------------------ Observer ------------------
class ISubscriber(ABC):
    @abstractmethod
    def update(self, channel_name: str, video_title: str):
        pass


# ------------------ Observable ------------------
class IChannel(ABC):
    @abstractmethod
    def subscribe(self, subscriber: ISubscriber):
        pass

    @abstractmethod
    def unsubscribe(self, subscriber: ISubscriber):
        pass

    @abstractmethod
    def notify_subscribers(self):
        pass


# ------------------ Concrete Subject ------------------
class Channel(IChannel):
    def __init__(self, name):
        self.name = name
        self._subscribers: List[ISubscriber] = []
        self._latest_video = ""

    def subscribe(self, subscriber: ISubscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: ISubscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber.update(self.name, self._latest_video)

    def upload_video(self, title: str):
        self._latest_video = title
        print(f'\n[{self.name} uploaded "{title}"]')
        self.notify_subscribers()


# ------------------ Concrete Observer ------------------
class Subscriber(ISubscriber):
    def __init__(self, name: str):
        self.name = name

    def update(self, channel_name: str, video_title: str):
        print(f"Hey {self.name}, check out {channel_name}'s new video: {video_title}")


# ------------------ Usage ------------------
if __name__ == "__main__":
    channel = Channel("CoderArmy")

    subs1 = Subscriber("Piyush")
    subs2 = Subscriber("Varun")

    channel.subscribe(subs1)
    channel.subscribe(subs2)

    channel.upload_video("Observer Design Pattern")
    channel.unsubscribe(subs1)
    channel.upload_video("Decorator Pattern Tutorial")