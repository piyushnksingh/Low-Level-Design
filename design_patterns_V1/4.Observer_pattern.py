# ============================================================
# OBSERVER PATTERN
# ============================================================
#
# Definition:
# Observer Pattern defines a ONE-TO-MANY relationship where
# one object notifies multiple dependent objects whenever
# its state/event changes.
#
#
# CORE IDEA:
#
# Observable → "Something changed."
# Observer   → "Tell me when something changes."
#
#
# ============================================================
# OBSERVABLE
# ============================================================
#
# Observable is the object whose state/event is being observed.
#
# It maintains a list of Observers and provides:
#
# attach() → subscribe an Observer
# detach() → unsubscribe an Observer
# notify() → notify all Observers
#
# Examples:
# - Order
# - YouTube Channel
# - Stock Price
# - Weather Station
#
#
# ============================================================
# OBSERVER
# ============================================================
#
# Observer is an object interested in changes/events of the
# Observable.
#
# It implements:
#
# update(data) → called when Observable changes
#
# Examples:
# - Email Notification
# - SMS Notification
# - Inventory Service
# - YouTube Subscriber
#
#
# ============================================================
# FLOW
# ============================================================
#
#                    Observable
#                        │
#                   state changes
#                        │
#                      notify()
#                        │
#            ┌───────────┼───────────┐
#            ↓           ↓           ↓
#        Observer 1  Observer 2  Observer 3
#            │           │           │
#         update()    update()    update()
#
#
# ============================================================
# WHY USE OBSERVER?
# ============================================================
#
# - One event can trigger multiple actions.
# - Avoid tight coupling between publisher and consumers.
# - Observers can be added/removed dynamically.
# - Observable doesn't need to know concrete Observer classes.
#
#
# ============================================================
# EXAMPLE
# ============================================================
#
# Order placed
#     ↓
# Order.notify()
#     ↓
# Email + SMS + Inventory
#
# The Order doesn't directly call:
#
#     email.send()
#     sms.send()
#     inventory.update()
#
# Instead, all of them subscribe as Observers.
#
#
# ============================================================
# OBSERVER vs STRATEGY
# ============================================================
#
# Strategy:
#     Choose ONE interchangeable behavior.
#
# Observer:
#     Notify MANY interested objects about a change.
#
# Strategy:
#     Payment → UPI OR Card OR Wallet
#
# Observer:
#     Order → Email + SMS + Inventory
#
#
# ============================================================
# WHEN TO THINK OBSERVER?
# ============================================================
#
# Look for:
# - One event/state change
# - Multiple components need to react
# - Subscribers/listeners can change dynamically
# - Want loose coupling between publisher and consumers
#
# Common examples:
# - Notifications
# - Event systems
# - Stock price updates
# - UI updates
# - Pub/Sub systems
#
#
# ============================================================
# INTERVIEW ONE-LINER:
#
# "Observer Pattern establishes a one-to-many relationship
# where the Observable notifies all registered Observers
# whenever its state or event changes."
#
# ============================================================

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass


class Subject(ABC):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)


class Order(Subject):
    def place_order(self, order_id):
        print(f"Order {order_id} placed")
        self.notify(order_id)


class EmailNotification(Observer):
    def update(self, data):
        print(f"Sent Email notification with: {data}")

class SMSNotification(Observer):
    def update(self, data):
        print(f"Sent SMS notification with: {data}")

class InventoryService(Observer):
    def update(self, data):
        print(f"Inventory updated for order: {data}")


def main():
    order = Order()
    inventory = InventoryService()
    email = EmailNotification()
    sms = SMSNotification()

    order.attach(inventory)
    order.attach(email)
    order.attach(sms)
    order.place_order("1")
    print("----------------------------")
    order.detach(inventory)
    order.place_order("2")


if __name__ == "__main__":
    main()




