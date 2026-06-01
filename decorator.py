from abc import ABC, abstractmethod

# ------------------ Component Interface ------------------
class Character(ABC):
    @abstractmethod
    def get_abilities(self):
        pass


# ------------------ Concrete Component ------------------
class Mario(Character):
    def get_abilities(self):
        return "Mario"


# ------------------ Abstract Decorator ------------------
class CharacterDecorator(Character):
    def __init__(self, character):
        self._character = character


# ------------------ Concrete Decorators ------------------
class HeightUp(CharacterDecorator):
    def get_abilities(self) -> str:
        return self._character.get_abilities() + " with HeightUp"


class GunPowerUp(CharacterDecorator):
    def get_abilities(self) -> str:
        return self._character.get_abilities() + " with Gun"


class StarPowerUp(CharacterDecorator):
    def get_abilities(self) -> str:
        return self._character.get_abilities() + " with Star Power (Limited Time)"


# ------------------ Client Code ------------------
if __name__ == '__main__':
    # Basic Mario
    mario = Mario()
    print("Basic Character:", mario.get_abilities())

    # Add HeightUp
    mario = HeightUp(mario)
    print("After HeightUp:", mario.get_abilities())

    # Add GunPowerUp
    mario = GunPowerUp(mario)
    print("After GunPowerUp:", mario.get_abilities())

    # Add StarPowerUp
    mario = StarPowerUp(mario)
    print("After StarPowerUp:", mario.get_abilities())

