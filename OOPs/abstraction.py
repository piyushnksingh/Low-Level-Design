from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def shift_gear(self, gear: int):
        pass

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def brake(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass

class SportsCar(Car):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.is_engine_on = False
        self.current_speed = 0
        self.current_gear = 0

    def start_engine(self):
        self.is_engine_on = True
        print(f"{self.brand} {self.model} : Engine starts with a roar!")

    def shift_gear(self, gear: int):
        if not self.is_engine_on:
            print(f"{self.brand} {self.model} : Engine is off! Cannot Shift Gear.")
            return
        self.current_gear = gear
        print(f"{self.brand} {self.model} : Shifted to gear {self.current_gear}")

    def accelerate(self):
        if not self.is_engine_on:
            print(f"{self.brand} {self.model} : Engine is off! Cannot accelerate.")
            return
        self.current_speed += 20
        print(f"{self.brand} {self.model} : Accelerating to {self.current_speed} km/h")

    def brake(self):
        self.current_speed -= 20
        if self.current_speed < 0:
            self.current_speed = 0
        print(f"{self.brand} {self.model} : Braking! Speed is now {self.current_speed} km/h")

    def stop_engine(self):
        self.is_engine_on = False
        self.current_gear = 0
        self.current_speed = 0
        print(f"{self.brand} {self.model} : Engine turned off.")


def main():
    car = SportsCar("Ford", "Mustang")
    car.start_engine()
    car.shift_gear(1)
    car.accelerate()
    car.shift_gear(2)
    car.accelerate()
    car.brake()
    car.stop_engine()

if __name__ == "__main__":
    main()
     