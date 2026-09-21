# COMMAND DESIGN PATTERN
#
# Purpose:
# Encapsulate a request/action as an object.
#
# Main benefit:
# Decouple the INVOKER from the RECEIVER.
#
# Command:
#   Defines execute() / undo()
#
# ConcreteCommand:
#   Connects the command to a Receiver.
#   Contains the actual operation to perform.
#
# Receiver:
#   Actually performs the business operation.
#
# Invoker:
#   Triggers the command.
#   Does NOT need to know how the operation works.
#
# Client:
#   Creates Receiver + ConcreteCommand
#   and assigns the command to the Invoker.
#
# Flow:
#
# Client
#   ↓
# creates Command with Receiver
#   ↓
# Invoker
#   ↓
# execute()
#   ↓
# ConcreteCommand
#   ↓
# Receiver
#
# Example:
#
# RemoteController → LightCommand → Light
#
# Without Command:
# RemoteController → Light
#
# With Command:
# RemoteController → Command → Light
#
# Why the extra layer?
# Because the action itself becomes an object.
# Therefore commands can be stored, queued, logged,
# scheduled, retried, or undone.

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class Light:
    def on(self):
        print("Light is ON !")

    def off(self):
        print("Light is OFF !")

class Fan:
    def on(self):
        print("Fan is ON !")

    def off(self):
        print("Fan is OFF !")


class LightCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class FanCommand(Command):
    def __init__(self, fan: Fan):
        self.fan = fan

    def execute(self):
        self.fan.on()

    def undo(self):
        self.fan.off()


class RemoteController:
    NUM_BUTTONS = 4

    def __init__(self):
        self.buttons = [None] * self.NUM_BUTTONS
        self.button_pressed = [False] * self.NUM_BUTTONS

    def set_command(self, idx: int, command: Command):
        if 0 <= idx < self.NUM_BUTTONS:
            self.buttons[idx] = command

    def press_button(self, idx: int):
        if not(0 <= idx < self.NUM_BUTTONS) or self.buttons[idx] is None:
            print(f"No command assigned at button {idx}")
            return

        if not self.button_pressed[idx]:
            self.buttons[idx].execute()
        else:
            self.buttons[idx].undo()

        self.button_pressed[idx] = not self.button_pressed[idx]


def main():
    light = Light()
    fan = Fan()

    remote = RemoteController()

    remote.set_command(0, LightCommand(light))
    remote.set_command(1, FanCommand(fan))

    remote.press_button(0)
    remote.press_button(0)

    remote.press_button(1)
    remote.press_button(1)

    remote.press_button(2)


if __name__ == "__main__":
    main()