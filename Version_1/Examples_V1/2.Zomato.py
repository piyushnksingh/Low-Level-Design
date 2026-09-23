from abc import ABC, abstractmethod

class MenuItem:
    def __init__(self, code: int, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    def get_name(self) -> str:
        return self._name

    def get_code(self) -> int:
        return self._code

    def get_price(self) -> int:
        return self._price

    def set_name(self, name):
        self._name = name

    def set_code(self, code):
        self._code = code

    def set_price(self, price):
        self._price = price

class Restaurant:
    _id = 0
    def __init__(self, name: str, location: str):
        Restaurant._id += 1
        self._restaurant_id = Restaurant._id
        self._name = name
        self._location = location
        self._menu_items: list[MenuItem] = []

    def get_name(self) -> str:
        return self._name

    def get_location(self) -> str:
        return self._location

    def get_menu_items(self) -> list[MenuItem]:
        return self._menu_items

    def set_name(self, name: str):
        self._name = name

    def set_location(self, location: str):
        self._location = location

    def set_menu_items(self, menu_item: MenuItem):
        self._menu_items.append(menu_item)

class Cart:
    