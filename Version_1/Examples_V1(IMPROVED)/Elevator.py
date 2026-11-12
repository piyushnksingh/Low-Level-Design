from enum import Enum
from abc import ABC, abstractmethod

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class RequestType(Enum):
    HALL = 1
    CAR = 2

class ElevatorState(Enum):
    IDLE = 1
    MOVING = 2
    DOOR_OPEN = 3
    OUT_OF_SERVICE = 4

class DoorState(Enum):
    OPEN = 1
    CLOSED = 2

class Request:
    def __init__(self, source_floor: int, direction: Direction,
                 request_type: RequestType, destination_floor = None):
        self.source_floor = source_floor
        self.direction = direction
        self.request_type = request_type
        self.destination_floor = destination_floor

    def get_request(self):
        return (
            f"Request(source={self.source_floor}, "
            f"direction={self.direction.name}, "
            f"type={self.request_type.name}, "
            f"destination={self.destination_floor})"
        )

class Door:
    def __init__(self):
        self.state = DoorState.CLOSED

    def open_door(self):
        if self.state == DoorState.CLOSED:
            self.state = DoorState.OPEN
            print("Door Opened !")

    def close_door(self):
        if self.state == DoorState.OPEN:
            self.state = DoorState.CLOSED
            print("Door Closed !")

    def is_door_open(self):
        return self.state == DoorState.OPEN

class Display:
    def __init__(self):
        self.current_floor = 0
        self.direction = Direction.IDLE

    def update(self, floor, direction):
        self.current_floor = floor
        self.direction = direction

    def display(self):
        print(f"Floor: {self.current_floor} | Direction: {self.direction.name}")


class Building:
    def __init__(self, total_floors: int, elevators: int):
        self.total_floors = total_floors
        self.elevators = elevators


class Elevator:
    def __init__(self, elevator_id: int, current_floor = 0):
        self.elevator_id = elevator_id
        self.current_floor = current_floor

        self.direction = Direction.IDLE
        self.state = ElevatorState.IDLE

        self.up_stops = set()
        self.down_stops = set()

        self.display = Display()
        self.door = Door()
        self.display.update(self.current_floor, self.direction)

    def add_request(self, request: Request):
        if request.request_type == RequestType.HALL:
            self.add



class Dispatcher:
    def __init__(self, elevators: list[Elevator]):
        self.elevators = elevators

    def assign_elevator(self):
        pass
