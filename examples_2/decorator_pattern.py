from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass

class RegularPizza(Pizza):
    def cost(self):
        return 100

    def description(self):
        return "Regular Pizza"

class LargePizza(Pizza):
    def cost(self):
        return 200

    def description(self):
        return "Large Pizza"



class PizzaDecorator(Pizza, ABC):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass


class Cheese(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 10

    def description(self):
        return f"{self._pizza.description()}, Cheese"

class Mushroom(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 20

    def description(self):
        return f"{self._pizza.description()}, Mushroom"

class Olives(PizzaDecorator):
    def cost(self):
        return self._pizza.cost() + 30

    def description(self):
        return f"{self._pizza.description()}, Olives"

if __name__ == "__main__":

    # Regular Pizza with Cheese + Mushroom + Olives
    regular_pizza = Olives(
                        Mushroom(
                            Cheese(
                                RegularPizza()
                            )
                        )
                    )

    print("Order:", regular_pizza.description())
    print("Total Cost:", regular_pizza.cost())

    print()

    # Large Pizza with Cheese + Olives
    large_pizza = Olives(
                        Cheese(
                            LargePizza()
                        )
                    )

    print("Order:", large_pizza.description())
    print("Total Cost:", large_pizza.cost())


