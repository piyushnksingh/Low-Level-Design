from abc import ABC, abstractmethod


# ------------------ Component ------------------
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass



# ------------------ Concrete Components (Base Coffees) ------------------
class Espresso(Coffee):
    def cost(self) -> float:
        return 80

    def description(self) -> str:
        return "Espresso"


class Cappuccino(Coffee):
    def cost(self) -> float:
        return 100

    def description(self) -> str:
        return "Cappuccino"


class Latte(Coffee):
    def cost(self) -> float:
        return 120

    def description(self) -> str:
        return "Latte"


# ------------------ Decorator Base ------------------
class AddOnDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# ------------------ Concrete Decorators ------------------
class Milk(AddOnDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 20

    def description(self) -> str:
        return self._coffee.description() + ", Milk"


class Sugar(AddOnDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 10

    def description(self) -> str:
        return self._coffee.description() + ", Sugar"


class Caramel(AddOnDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 25

    def description(self) -> str:
        return self._coffee.description() + ", Caramel"


class WhippedCream(AddOnDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 30

    def description(self) -> str:
        return self._coffee.description() + ", Whipped Cream"





# ------------------ Client Code ------------------
if __name__ == "__main__":
    # Example 1
    coffee1 = Espresso()
    coffee1 = Milk(coffee1)
    coffee1 = Caramel(coffee1)
    coffee1 = Milk(coffee1)

    print("Order 1:")
    print("Description:", coffee1.description())
    print("Cost:", coffee1.cost())

    print()

    # Example 2 (with size)
    coffee2 = Latte()
    coffee2 = WhippedCream(coffee2)
    coffee2 = Sugar(coffee2)

    print("Order 2:")
    print("Description:", coffee2.description())
    print("Cost:", coffee2.cost())
