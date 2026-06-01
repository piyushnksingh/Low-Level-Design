class ManualCar:
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model
        self._is_engine_on = False
        self._current_speed = 0
        self._current_gear = 0

    def start_engine(self):
        self._is_engine_on = True
        print(f"{self._brand} {self._model} : Engine started.")

    def stop_engine(self):
        self._is_engine_on = False
        self._current_speed = 0
        print(f"{self._brand} {self._model} : Engine turned off.")

    # Simulating method overloading
    def accelerate(self, speed=None):
        if not self._is_engine_on:
            print(f"{self._brand} {self._model} : Cannot accelerate! Engine is off.")
            return

        if speed is None:
            self._current_speed += 20
        else:
            self._current_speed += speed

        print(f"{self._brand} {self._model} : Accelerating to {self._current_speed} km/h")

    def brake(self):
        self._current_speed -= 20
        if self._current_speed < 0:
            self._current_speed = 0
        print(f"{self._brand} {self._model} : Braking! Speed is now {self._current_speed} km/h")

    def shift_gear(self, gear):
        self._current_gear = gear
        print(f"{self._brand} {self._model} : Shifted to gear {self._current_gear}")


# Main
if __name__ == "__main__":
    my_manual_car = ManualCar("Suzuki", "WagonR")
    my_manual_car.start_engine()
    my_manual_car.accelerate()       # default behavior
    my_manual_car.accelerate(40)     # custom speed
    my_manual_car.brake()
    my_manual_car.stop_engine()










