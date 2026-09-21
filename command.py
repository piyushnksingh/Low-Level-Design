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
        print("Light ON !!")

    def off(self):
        print("Light OFF !!")

class Fan:
    def on(self):
        print("Fan ON !!")

    def off(self):
        print("Fan OFF !!")

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


class RemoteControl:
    NUM_BUTTONS = 4
    def __init__(self):
        self.buttons = [None] * self.NUM_BUTTONS
        self.button_pressed = [False] * self.NUM_BUTTONS

    def set_command(self, idx: int, command: Command):
        if idx < 0 or idx >= self.NUM_BUTTONS:
            print("Invalid button")
            return

        self.buttons[idx] = command

    def press_button(self, idx: int):
        if idx < 0 or idx >= self.NUM_BUTTONS or self.buttons[idx] is None:
            print("Invalid button")
            return

        if self.button_pressed[idx] is False:
            self.buttons[idx].execute()
        else:
            self.buttons[idx].undo()

        self.button_pressed[idx] = not self.button_pressed[idx]


def main():
    light = Light()
    fan = Fan()

    light_command = LightCommand(light)
    fan_command = FanCommand(fan)

    remote_control = RemoteControl()

    remote_control.set_command(0, light_command)
    remote_control.set_command(1, fan_command)

    remote_control.press_button(0)
    remote_control.press_button(0)

    remote_control.press_button(1)
    remote_control.press_button(1)


if __name__ == "__main__":
    main()