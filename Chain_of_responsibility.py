# from abc import ABC, abstractmethod
#
# class LeaveHandler(ABC):
#     def __init__(self, can_approve_days: int):
#         self.can_approve_days = can_approve_days
#         self.next_handler = None
#
#     def set_handler(self, handler):
#         self.next_handler = handler
#
#     @abstractmethod
#     def handle_leaves(self, num_of_days):
#         pass
#
# class ManagerHandler(LeaveHandler):
#     def handle_leaves(self, num_of_days):
#         if num_of_days <= 0:
#             print("leaves cannot be less than 0 !")
#             return
#
#         if num_of_days <= self.can_approve_days:
#             print("leaves approved by manager")
#         else:
#             self.next_handler.handle_leaves(num_of_days)
#
# class DirectorHandler(LeaveHandler):
#     def handle_leaves(self, num_of_days):
#         if num_of_days <= self.can_approve_days:
#             print("leaves approved by director")
#         else:
#             self.next_handler.handle_leaves(num_of_days)
#
# class VPHandler(LeaveHandler):
#     def handle_leaves(self, num_of_days):
#         if num_of_days <= self.can_approve_days:
#             print("leaves approved by VP")
#         else:
#             print(f"leave of {num_of_days} days cannot be approved !!")
#
#
# def main():
#     manager_handler = ManagerHandler(2)
#     director_handler = DirectorHandler(5)
#     vp_handler = VPHandler(10)
#
#     manager_handler.set_handler(director_handler)
#     director_handler.set_handler(vp_handler)
#
#     leaves_days = 90
#
#     manager_handler.handle_leaves(leaves_days)
#
# if __name__ == "__main__":
#     main()


# -----------------------------------------------   OPTIMIZED  --------------------------------------------

from dataclasses import dataclass
from datetime import date


@dataclass
class LeaveRequest:
    employee_id: int
    start_date: date
    end_date: date
    num_of_days: int
    leave_type: str


class LeaveHandler:

    def __init__(self, role, can_approve_days):
        self.role = role
        self.can_approve_days = can_approve_days
        self.next_handler = None

    def set_next_handler(self, handler):
        self.next_handler = handler
        return handler

    def handle_leave(self, request: LeaveRequest):

        if request.num_of_days <= 0:
            print("Invalid leave request")
            return

        if request.num_of_days <= self.can_approve_days:
            print(f"Leave approved by {self.role}")
            return

        if self.next_handler:
            self.next_handler.handle_leave(request)
        else:
            print(f"Leave of {request.num_of_days} days cannot be approved")

def main():
    manager = LeaveHandler("Manager", 2)
    director = LeaveHandler("Director", 5)
    vp = LeaveHandler("VP", 10)

    manager.set_next_handler(director)
    director.set_next_handler(vp)

    request = LeaveRequest(
        employee_id=101,
        start_date=date(2026, 9, 20),
        end_date=date(2026, 9, 24),
        num_of_days=8,
        leave_type="CASUAL"
    )

    manager.handle_leave(request)

if __name__ == "__main__":
    main()