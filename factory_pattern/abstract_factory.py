# https://youtu.be/dMK4TbG29fk?si=86Rm1d-T7gRgQCAm

from abc import ABC, abstractmethod

# ------------------ Product 1: Burger ------------------
class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


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


# ------------------ Product 2: Garlic Bread ------------------
class GarlicBread(ABC):
    @abstractmethod
    def prepare(self):
        pass


class BasicGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Basic Garlic Bread with butter and garlic!")


class CheeseGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Cheese Garlic Bread with extra cheese and butter!")


class BasicWheatGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Basic Wheat Garlic Bread with butter and garlic!")


class CheeseWheatGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Cheese Wheat Garlic Bread with extra cheese and butter!")


# ------------------ Abstract Factory ------------------
class MealFactory(ABC):
    @abstractmethod
    def create_burger(self, burger_type: str):
        pass

    @abstractmethod
    def create_garlic_bread(self, bread_type: str):
        pass


# ------------------ Concrete Factories ------------------
class SinghBurger(MealFactory):
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

    def create_garlic_bread(self, bread_type: str):
        if bread_type == "basic":
            return BasicGarlicBread()
        elif bread_type == "cheese":
            return CheeseGarlicBread()
        else:
            print("Invalid garlic bread type!")
            return None


class KingBurger(MealFactory):
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

    def create_garlic_bread(self, bread_type: str):
        if bread_type == "basic":
            return BasicWheatGarlicBread()
        elif bread_type == "cheese":
            return CheeseWheatGarlicBread()
        else:
            print("Invalid garlic bread type!")
            return None


# ------------------ Main ------------------
if __name__ == "__main__":
    burger_type = "basic"
    garlic_bread_type = "cheese"

    king_factory = KingBurger()
    burger = king_factory.create_burger(burger_type)
    garlic_bread = king_factory.create_garlic_bread(garlic_bread_type)
    if burger:
        burger.prepare()
    if garlic_bread:
        garlic_bread.prepare()

    singh_factory = SinghBurger()
    burger = singh_factory.create_burger(burger_type)
    garlic_bread = singh_factory.create_garlic_bread(garlic_bread_type)
    if burger:
        burger.prepare()
    if garlic_bread:
        garlic_bread.prepare()