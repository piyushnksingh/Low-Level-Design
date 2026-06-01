class SportsCar:
    def __init__(self, brand, model):
        self.__brand = brand  # __ means name mangling, but can be accessed from outside.
        self.__model = model
        self.__is_engine_on = False
        self.__current_speed = 0
        self.__current_gear = 0
        self.__tyre_company = "MRF"

    # Getter for speed
    def get_speed(self):
        return self.__current_speed

    # Getter for tyre company
    def get_tyre_company(self):
        return self.__tyre_company

    # Setter for tyre company
    def set_tyre_company(self, tyre_company):
        self.__tyre_company = tyre_company

    def start_engine(self):
        self.__is_engine_on = True
        print(f"{self.__brand} {self.__model} : Engine starts with a roar!")

    def shift_gear(self, gear):
        if not self.__is_engine_on:
            print(f"{self.__brand} {self.__model} : Engine is off! Cannot Shift Gear.")
            return
        self.__current_gear = gear
        print(f"{self.__brand} {self.__model} : Shifted to gear {self.__current_gear}")

    def accelerate(self):
        if not self.__is_engine_on:
            print(f"{self.__brand} {self.__model} : Engine is off! Cannot accelerate.")
            return
        self.__current_speed += 20
        print(f"{self.__brand} {self.__model} : Accelerating to {self.__current_speed} km/h")

    def brake(self):
        self.__current_speed -= 20
        if self.__current_speed < 0:
            self.__current_speed = 0
        print(f"{self.__brand} {self.__model} : Braking! Speed is now {self.__current_speed} km/h")

    def stop_engine(self):
        self.__is_engine_on = False
        self.__current_gear = 0
        self.__current_speed = 0
        print(f"{self.__brand} {self.__model} : Engine turned off.")


# Main
if __name__ == "__main__":
    my_sports_car = SportsCar("Ford", "Mustang")

    my_sports_car.start_engine()
    my_sports_car.shift_gear(1)
    my_sports_car.accelerate()
    my_sports_car.shift_gear(2)
    my_sports_car.accelerate()
    my_sports_car.brake()
    my_sports_car.stop_engine()

    my_sports_car.__brand = "aaaaaaaaaaaaa" # create a new variable , doesn't modify the private brand attribute
    print(my_sports_car._SportsCar__brand)  # 👉 Ford (original)
    print(my_sports_car.__brand)  # 👉 aaaaaaaaaaaaa (new one)


    print("Current Speed of My Sports Car is", my_sports_car.get_speed())