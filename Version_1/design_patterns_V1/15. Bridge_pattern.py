"""
1. Intent / Definition
Bridge Pattern decouples an abstraction (High-Level Layer) from its implementation (Low-Level Layer) so that both can vary independently.

2. Problem – Class Explosion
Consider a Car with:
- Car Types: Sedan, SUV, Hatchback (m types)
- Engines: Petrol, Diesel, Electric (n types)

If we create a separate class for every combination:
- SedanPetrol, SedanDiesel, SedanElectric
- SUVPetrol, SUVDiesel, SUVElectric
- HatchbackPetrol, HatchbackDiesel, HatchbackElectric

Total classes = m × n.

This leads to Class Explosion, increased complexity, code duplication and reduced reusability.

3. Solution – Bridge Pattern
Split the design into two independent hierarchies:

High-Level Layer (Abstraction):
- Car
- Sedan, SUV

Low-Level Layer (Implementation):
- Engine
- Petrol, Diesel, Electric
- Car maintains a reference to Engine (HAS-A relationship).
- Car defines drive().
- Engine defines start().
- Concrete classes override their respective methods.
- Inject any Engine implementation into any Car type.

Result: m × n classes → m + n classes.

4. UML Structure
- Abstraction: High-level interface/class.
- Refined Abstraction: Concrete high-level classes.
- Implementor: Low-level interface/class.
- Concrete Implementor: Concrete low-level implementations.

The Abstraction maintains a reference to the Implementor and delegates implementation-specific work to it.

5. Example – Car & Engine
my_sedan = Sedan(PetrolEngine())
my_suv = SUV(ElectricEngine())
your_suv = SUV(DieselEngine())

Here, Car doesn't need to know which engine is injected. It simply calls:
self.engine.start()

Both hierarchies can evolve independently.

6. Bridge vs Strategy Pattern

Their UML diagrams can look almost identical. The primary difference is their intent.

Bridge:

- Separates abstraction from implementation.
- Focuses on independent evolution of two hierarchies.
- Both hierarchies can grow independently.
- Pairing is generally established during object creation.

Strategy:

- Encapsulates interchangeable algorithms.
- Focuses on switching algorithms/behaviours.
- Client can interchange strategies dynamically.
- Strategy can be changed at runtime.

Example:

- Bridge: Sedan + Petrol Engine. Focus is supporting new car types and engines independently.
- Strategy: Switching an SUV from Petrol to Diesel strategy dynamically.

7. Real-World Use Cases
8. Remote & TV
   - Abstraction: Different remotes.
   - Implementation: Different TVs.
   - Any remote can work with different TV types.
9. GUI & Operating Systems
   - Abstraction: TextBox, Dropdown, RadioButton.
   - Implementation: Windows, macOS, Linux.
   - GUI components can work across different operating systems.
10. When to Use?

- When you have two independent dimensions of variation.
- When inheritance leads to class explosion.
- When you want abstraction and implementation to evolve independently.
- When you want to avoid tightly coupled hierarchies.

Interview one-liner:
Bridge Pattern uses composition over inheritance to separate abstraction from implementation, allowing both to vary independently and preventing class explosion.
"""


from abc import ABC, abstractmethod

# Implementation Hierarchy (Low-Level Layer)
class Engine(ABC):
    @abstractmethod
    def start(self):
        pass

# Concrete Implementors
class PetrolEngine(Engine):
    def start(self):
        print("Petrol engine starting with ignition!")

class DieselEngine(Engine):
    def start(self):
        print("Diesel engine roaring to life!")


class ElectricEngine(Engine):
    def start(self):
        print("Electric engine powering up silently!")

# Abstraction Hierarchy (High-Level Layer)
class Car(ABC):
    def __init__(self, engine: Engine):
        self.engine = engine

    @abstractmethod
    def drive(self):
        pass

# Refined Abstraction
class Sedan(Car):
    def drive(self):
        self.engine.start()
        print("Driving a Sedan on the highway.")

class SUV(Car):
    def drive(self):
        self.engine.start()
        print("Driving an SUV off-road.")

# Client Code
if __name__ == "__main__":

    # Create Engine implementations
    petrol_eng = PetrolEngine()
    diesel_eng = DieselEngine()
    electric_eng = ElectricEngine()

    # Create Car objects with dependency injection
    my_sedan = Sedan(petrol_eng)
    my_suv = SUV(electric_eng)
    your_suv = SUV(diesel_eng)

    # Use the cars
    my_sedan.drive()
    my_suv.drive()
    your_suv.drive()