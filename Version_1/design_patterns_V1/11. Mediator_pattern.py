from abc import ABC, abstractmethod


class IMediator(ABC):
    @abstractmethod
    def send_all(self, sender: str, msg: str):
        pass

    @abstractmethod
    def send_private(self, sender: str, receiver: str, msg: str):
        pass

    @abstractmethod
    def register_colleague(self, colleague):
        pass

class ChatMediator(IMediator):
    def __init__(self):
        self._colleagues = []
        self._mutes = []  # (muter, muted)

    def send_all(self, sender: str, msg: str):
        print(f"[{sender} broadcasts]: {msg}")
        for colleague in self._colleagues:
            if colleague.get_name() == sender:
                continue

            is_muted = False
            for muter, muted in self._mutes:
                if colleague.get_name() == muter and sender == muted:
                    is_muted = True
                    break

            if not is_muted:
                colleague.receive(sender, msg)

    def send_private(self, sender, receiver, msg):
        print(f"[{sender} → {receiver}]: {msg}")
        for colleague in self._colleagues:
            if colleague.get_name() == receiver:
                for muter, muted in self._mutes:
                    if muter == receiver and muted == sender:
                        print("\n[Message is muted]")
                        return

                colleague.receive(sender, msg)
                return

        print(f'[Mediator] User "{receiver}" not found')

    def register_colleague(self, colleague):
        self._colleagues.append(colleague)

    def mute(self, who, whom):
        self._mutes.append((who, whom))

class Colleague(ABC):
    def __init__(self, mediator: IMediator):
        self._mediator = mediator
        self._mediator.register_colleague(self)

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def send_all(self, msg):
        pass

    @abstractmethod
    def send_private(self, receiver: str, msg: str):
        pass

    @abstractmethod
    def receive(self, sender: str, msg: str):
        pass

class User(Colleague):
    def __init__(self, name: str, mediator: IMediator):
        super().__init__(mediator)
        self._mediator = mediator
        self._name = name

    def get_name(self):
        return self._name

    def send_all(self, msg):
        return self._mediator.send_all(self._name, msg)

    def send_private(self, receiver: str, msg: str):
        return self._mediator.send_private(self._name, receiver, msg)

    def receive(self, sender: str, msg: str):
        print(f"    {self._name} got from {sender}: {msg}")


def main():
    chat_room = ChatMediator()

    user1 = User("Rohan", chat_room)
    user2 = User("Neha", chat_room)
    user3 = User("Mohan", chat_room)

    chat_room.mute("Rohan", "Mohan")

    user1.send_all("Hello EveryOne !")

    user3.send_private("Neha", "Hey Neha !")

if __name__ == "__main__":
    main()



