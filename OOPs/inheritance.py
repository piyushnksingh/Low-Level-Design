class Car:
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model
        self._is_engine_on = False
        self._current_speed = 0

    # Common methods for all cars
    def start_engine(self):
        self._is_engine_on = True
        print(f"{self._brand} {self._model} : Engine started.")

    def stop_engine(self):
        self._is_engine_on = False
        self._current_speed = 0
        print(f"{self._brand} {self._model} : Engine turned off.")

    def accelerate(self):
        if not self._is_engine_on:
            print(f"{self._brand} {self._model} : Cannot accelerate! Engine is off.")
            return
        self._current_speed += 20
        print(f"{self._brand} {self._model} : Accelerating to {self._current_speed} km/h")

    def brake(self):
        self._current_speed -= 20
        if self._current_speed < 0:
            self._current_speed = 0
        print(f"{self._brand} {self._model} : Braking! Speed is now {self._current_speed} km/h")


class ManualCar(Car):  # Inherits from Car
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._current_gear = 0

    # Specialized method
    def shift_gear(self, gear):
        self._current_gear = gear
        print(f"{self._brand} {self._model} : Shifted to gear {self._current_gear}")


class ElectricCar(Car):  # Inherits from Car
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._battery_level = 100

    # Specialized method
    def charge_battery(self):
        self._battery_level = 100
        print(f"{self._brand} {self._model} : Battery fully charged!")


# Main
if __name__ == "__main__":
    my_manual_car = ManualCar("Suzuki", "WagonR")
    my_manual_car.start_engine()
    my_manual_car.shift_gear(1)  # specific to manual car
    my_manual_car.accelerate()
    my_manual_car.brake()
    my_manual_car.stop_engine()

    print("----------------------")

    my_electric_car = ElectricCar("Tesla", "Model S")
    my_electric_car.charge_battery()  # specific to electric car
    my_electric_car.start_engine()
    my_electric_car.accelerate()
    my_electric_car.brake()
    my_electric_car.stop_engine()