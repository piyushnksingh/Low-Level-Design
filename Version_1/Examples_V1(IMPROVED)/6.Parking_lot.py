from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from enum import Enum
from math import ceil
from threading import Lock
from uuid import uuid4


class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class ParkingSlotType(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3

class TicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
    COMPLETED = 3

class ParkingLotException(Exception):
    pass

class InvalidVehicleException(ParkingLotException):
    pass

class NoParkingSpotAvailableException(ParkingLotException):
    pass

class InvalidTicketException(ParkingLotException):
    pass

class PaymentFailedException(ParkingLotException):
    pass

class Vehicle(ABC):
    def __init__(self, license_plate: str):
        if not license_plate:
            raise InvalidVehicleException("Invalid License Plate !")
        self.license_plate = license_plate

    @abstractmethod
    def get_type(self):
        pass

class Motorcycle(Vehicle):
    def get_type(self):
        return VehicleType.MOTORCYCLE

class Car(Vehicle):
    def get_type(self):
        return VehicleType.CAR

class Bus(Vehicle):
    def get_type(self):
        return VehicleType.BUS

class ParkingSpot(ABC):
    def __init__(self, spot_id: str, floor_id: str):
        self.spot_id = spot_id
        self.floor_id = floor_id
        self.vehicle = None
        self._lock = Lock()

    @abstractmethod
    def spot_type(self):
        pass

    @abstractmethod
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        pass

    def is_available(self) -> bool:
        return self.vehicle is None

    def park_vehicle(self, vehicle: Vehicle):
        with self._lock:
            if not self.is_available():
                raise ParkingLotException("Spot Already Occupied !")

            if not self.can_accommodate(vehicle):
                raise InvalidVehicleException("Vehicle cannot fit in this spot")

            self.vehicle = vehicle

    def remove_vehicle(self):
        with self._lock:
            if self.is_available():
                raise ParkingLotException("Spot is already empty")

            vehicle = self.vehicle
            self.vehicle = None
            return vehicle


class MotorcycleSpot(ParkingSpot):
    def spot_type(self):
        return ParkingSlotType.MOTORCYCLE

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.get_type() == VehicleType.MOTORCYCLE

class CompactSpot(ParkingSpot):
    def spot_type(self):
        return ParkingSlotType.COMPACT

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.get_type() in {
            VehicleType.MOTORCYCLE,
            VehicleType.CAR
        }

class LargeSpot(ParkingSpot):
    def spot_type(self):
        return ParkingSlotType.LARGE

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        return vehicle.get_type() in {
            VehicleType.CAR,
            VehicleType.MOTORCYCLE,
            VehicleType.BUS
        }

class ParkingFloor:
    def __init__(self, floor_id: str):
        self.floor_id = floor_id
        self.spots = []

    def get_available_spots(self):
        return [
            spot for spot in self.spots
            if spot.is_available()
        ]

    def add_spot(self, spot: ParkingSpot):
        if spot.floor_id != self.floor_id:
            raise ParkingLotException("Spot belongs to another floor !")
        if any(s.spot_id == spot.spot_id for s in self.spots):
            raise ParkingLotException("Duplicate parking slot ID")

        self.spots.append(spot)

class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, parking_lot, vehicle):
        pass

class FirstAvailableSpotStrategy(SpotAllocationStrategy):
    def find_spot(self, parking_lot, vehicle: Vehicle):
        for floor in parking_lot.floors:
            for spot in floor.spots:
                if spot.is_available() and spot.can_accommodate(vehicle):
                    return spot

        return None

class NearestAvailableSpotStrategy(SpotAllocationStrategy):
    def find_spot(self, parking_lot, vehicle: Vehicle):
        return FirstAvailableSpotStrategy().find_spot(parking_lot, vehicle)

class Ticket:
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot):
        self.ticket_id = str(uuid4())
        self.vehicle = vehicle
        self.parking_spot = parking_spot

        self.entry_time = datetime.now()
        self.exit_time = None

        self.amount = 0.0
        self.status = TicketStatus.ACTIVE

        # Prevent concurrent processing of the same ticket.
        self._lock = Lock()

class ParkingLot:
    def __init__(self, lot_id: str, allocation_strategy: SpotAllocationStrategy):
        self.lot_id = lot_id
        self.floors = []


        self.allocation_strategy = allocation_strategy
        self.active_tickets = {}

        # Protects allocation and ticket registration.
        self._lock = Lock()

    def add_floor(self, floor: ParkingFloor):
        if any(f.floor_id == floor.floor_id for f in self.floors):
            raise ParkingLotException("Duplicate Floor id")

        self.floors.append(floor)

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        with self._lock:
            spot = self.allocation_strategy.find_spot(self, vehicle)

            if spot is None:
                raise NoParkingSpotAvailableException(
                    "No suitable parking spot available")

            spot.park_vehicle(vehicle)
            ticket = Ticket(vehicle, spot)
            self.active_tickets[ticket.ticket_id] = ticket
            return ticket

    def release_spot(self, ticket: Ticket):
        with self._lock:
            current_ticket = self.active_tickets.get(ticket.ticket_id)
            if current_ticket is not ticket:
                raise InvalidTicketException("Invalid Ticket !")

            ticket.parking_spot.remove_vehicle()
            del self.active_tickets[ticket.ticket_id]

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> Decimal:
        pass

class HourlyPricingStrategy(PricingStrategy):
    def __init__(self, hourly_rate: Decimal):
        self.hourly_rate = hourly_rate

    def calculate_fee(self, ticket: Ticket) -> Decimal:
        end_time = ticket.exit_time or datetime.now()
        duration = end_time - ticket.entry_time
        hours = max(1, ceil(duration.total_seconds() / 3600))
        return self.hourly_rate * hours

class VehicleBasedPricingStrategy(PricingStrategy):
    def __init__(self):
        self.hourly_rate = {
            VehicleType.MOTORCYCLE: Decimal("10"),
            VehicleType.CAR: Decimal("20"),
            VehicleType.BUS: Decimal("50")
        }

    def calculate_fee(self, ticket: Ticket) -> Decimal:
        exit_time = datetime.now() or ticket.exit_time
        duration = exit_time - ticket.entry_time
        hours = max(1, ceil(duration.total_seconds() / 3600))
        rate = self.hourly_rate[ticket.vehicle.get_type()]
        return rate * hours

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: Decimal):
        pass

class CardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: Decimal):
        print(f"Processing payment: rs. {amount}")
        return True

class EntryGate:
    def __init__(self, gate_id: str, parking_lot: ParkingLot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def enter_vehicle(self, vehicle: Vehicle) -> Ticket:
        ticket = self.parking_lot.park_vehicle(vehicle)

        print(f"Vehicle {vehicle.license_plate} parked"
              f" at floor {ticket.parking_spot.floor_id}"
              f"spot {ticket.parking_spot.spot_id}")

        return ticket

class ExitGate:
    def __init__(self, gate_id: str, parking_lot: ParkingLot, pricing_strategy: PricingStrategy,
                 payment_processor: PaymentProcessor):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

        self.pricing_strategy = pricing_strategy
        self.payment_processor = payment_processor

    def exit_vehicle(self, ticket: Ticket) -> Decimal:
        with ticket._lock:
            if ticket.status != TicketStatus.ACTIVE:
                raise InvalidTicketException(
                    "Ticket is not active"
                )

            if self.parking_lot.active_tickets.get(
                    ticket.ticket_id
            ) is not ticket:
                raise InvalidTicketException("Invalid ticket")

            ticket.exit_time = datetime.now()

            amount = self.pricing_strategy.calculate_fee(ticket)

            print(f"Parking fee: Rs. {amount}")

            payment_success = self.payment_processor.process_payment(amount)

            if not payment_success:
                ticket.exit_time = None
                raise PaymentFailedException(
                    "Payment failed. Please retry."
                )

            ticket.amount = amount
            ticket.status = TicketStatus.PAID

            self.parking_lot.release_spot(ticket)
            ticket.status = TicketStatus.COMPLETED

            print(
                f"Vehicle {ticket.vehicle.license_plate} exited successfully"
            )

            return amount


if __name__ == "__main__":

    # Create parking lot
    allocation_strategy = FirstAvailableSpotStrategy()

    parking_lot = ParkingLot(
        "LOT_01",
        allocation_strategy
    )

    # Create floors
    floor_1 = ParkingFloor("F1")
    floor_2 = ParkingFloor("F2")

    # Add spots to floor 1
    floor_1.add_spot(MotorcycleSpot("M1", "F1"))
    floor_1.add_spot(CompactSpot("C1", "F1"))
    floor_1.add_spot(LargeSpot("L1", "F1"))

    # Add spots to floor 2
    floor_2.add_spot(MotorcycleSpot("M2", "F2"))
    floor_2.add_spot(CompactSpot("C2", "F2"))
    floor_2.add_spot(LargeSpot("L2", "F2"))

    parking_lot.add_floor(floor_1)
    parking_lot.add_floor(floor_2)

    # Create gates
    entry_gate_1 = EntryGate("ENTRY_01", parking_lot)
    entry_gate_2 = EntryGate("ENTRY_02", parking_lot)

    exit_gate_1 = ExitGate(
        "EXIT_01",
        parking_lot,
        VehicleBasedPricingStrategy(),
        CardPaymentProcessor()
    )

    exit_gate_2 = ExitGate(
        "EXIT_02",
        parking_lot,
        VehicleBasedPricingStrategy(),
        CardPaymentProcessor()
    )

    # Vehicle entry
    car = Car("TS09AB1234")
    motorcycle = Motorcycle("TS09CD5678")
    bus = Bus("TS09EF9012")

    car_ticket = entry_gate_1.enter_vehicle(car)

    motorcycle_ticket = entry_gate_2.enter_vehicle(
        motorcycle
    )

    bus_ticket = entry_gate_1.enter_vehicle(bus)

    # Vehicle exit
    exit_gate_1.exit_vehicle(car_ticket)

    exit_gate_2.exit_vehicle(motorcycle_ticket)

    exit_gate_1.exit_vehicle(bus_ticket)





























