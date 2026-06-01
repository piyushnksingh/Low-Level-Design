from abc import ABC, abstractmethod

# --- Abstract Burger ---
class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


# --- Concrete Burgers ---
class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# --- Factory ---
class BurgerFactory:
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


# --- Main ---
if __name__ == "__main__":
    burger_type = "premium"

    factory = BurgerFactory()
    burger = factory.create_burger(burger_type)

    if burger:
        burger.prepare()