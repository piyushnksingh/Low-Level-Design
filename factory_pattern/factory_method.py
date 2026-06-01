from abc import ABC, abstractmethod

# --- Product Base ---
class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


# --- Concrete Products ---
class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


class BasicWheatBurger(Burger):
    def prepare(self):
        print("Preparing Basic Wheat Burger with bun, patty, and ketchup!")


class StandardWheatBurger(Burger):
    def prepare(self):
        print("Preparing Standard Wheat Burger with bun, patty, cheese, and lettuce!")


class PremiumWheatBurger(Burger):
    def prepare(self):
        print("Preparing Premium Wheat Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# --- Abstract Factory ---
class BurgerFactory(ABC):
    @abstractmethod
    def create_burger(self, burger_type: str):
        pass


# --- Concrete Factories ---
class SinghBurger(BurgerFactory):
    def create_burger(self, burger_type: str):
        if burger_type == "basic":
            return BasicBurger()
        elif burger_type == "standard":
            return StandardBurger()
        elif burger_type == "premium":
            return PremiumBurger()
        else:
            print("Invalid burger type!")
            return None


class KingBurger(BurgerFactory):
    def create_burger(self, burger_type: str):
        if burger_type == "basic":
            return BasicWheatBurger()
        elif burger_type == "standard":
            return StandardWheatBurger()
        elif burger_type == "premium":
            return PremiumWheatBurger()
        else:
            print("Invalid burger type!")
            return None


# --- Main ---
if __name__ == "__main__":
    burger_type = "basic"

    singh_factory = SinghBurger()
    burger = singh_factory.create_burger(burger_type)
    if burger:
        burger.prepare()

    king_factory = KingBurger()
    burger = king_factory.create_burger(burger_type)
    if burger:
        burger.prepare()