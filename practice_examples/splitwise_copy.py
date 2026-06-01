from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum
from typing import List

class Split:
    def __init__(self, user_id : str, amount: float):
        self.user_id = user_id
        self.amount = amount


class SplitType(Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"


class ISplitStrategy(ABC):
    @abstractmethod
    def calculate_split(self, total: float, user_ids: List[str],
                        values: List[float] = None) -> List[Split]:
        pass


class EqualSplit(ISplitStrategy):
    def calculate_split(self, total: float, user_ids: List[str],
                        values: List[float] = None) -> List[Split]:
        amount = total / len(user_ids)
        return [Split(user_id, amount) for user_id in user_ids]
.l,kmn .n

class ExactSplit(ISplitStrategy):
    def calculate_split(self, total: float, user_ids: List[str],
                        values: List[float] = None) -> List[Split]:

        return [Split(user_ids[i], values[i]) for i in range(len(user_ids))]


class PercentageSplit(ISplitStrategy):
    def calculate_split(self, total, user_ids, values=None):
        return [Split(user_ids[i], total * values[i] / 100) for i in range(len(user_ids))]


class SplitFactory:
    @staticmethod
    def split(split_strategy: ISplitStrategy):
        if split_strategy == SplitType.EXACT:
            return ExactSplit()
        elif split_strategy == SplitType.PERCENTAGE:
            return PercentageSplit()
        else:
            return EqualSplit()  # default to Equal split


class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class User(IObserver):
    _id = 0

    def __init__(self, user_name, email):
        User._id += 1
        self.user_id = f"user_{User._id}"
        self.user_name = user_name
        self.email = email
        self.balances = defaultdict(float)  # map

    def update(self, msg: str):
        print(f"[NOTIFICATION to {self.user_name}]: {msg}")

    def update_balance(self, amount: float, other: List[str]):
        self.balances[other] += amount
        if abs(self.balances[other]) < 0.01:
            del self.balances[other]

    def get_total_owed(self):
        return sum(abs(v) for v in self.balances.values() if v < 0)

    def get_total_owing(self):
        return sum(v for v in self.balances.values() if v > 0)


class Expense:
    _id = 0
    def __init__(self, desc, amount, paid_by, splits, group_id = ""):
        Expense._id += 1
        self._id = Expense._id
        self.desc = desc
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits
        self.group_id = group_id


class DebtSimplifier:
    @staticmethod
    def simplify(group_balances):
        net = defaultdict(float)

        for u in group_balances:
            for v, amt in group_balances[u].items():
                if amt > 0:
                    net[u] += amt
                    net[v] -= amt

        creditors = []
        debitors = []
        for u, amt in net.items():
            if amt > 0:
                creditors.append([u, amt])
            else:
                debitors.append([u, -amt])

        creditors.sort(key = lambda x: -x[1])
        debitors.sort(key = lambda x: -x[1])

        result = {u : {} for u in group_balances}

        i = j = 0

        while i < len(creditors) and j < len(debitors):
            c_id, c_amt = creditors[i]
            d_id, d_amt = debitors[j]

            settle = min(c_amt, d_amt)

            result[c_id][d_id] = settle
            result[d_id][c_id] = -settle

            creditors[i][1] -= settle
            debitors[j][1] -= settle

            if creditors[i][1] < 0.01:
                i += 1
            if debitors[j][1] < 0.01:
                j += 1

        return result


class Group:
    _id = 0
    def __init__(self, group_name):
        Group._id += 1
        self._id = Group._id
        self.group_name = group_name
        self.members = []
        self.balances = defaultdict(lambda : defaultdict(float))

    def add_member(self, user: User):
        self.members.append(user)

    def remove_member(self, user: User):
        self.members.remove(user)

    def notify(self, msg: str):
        for user in self.members:
            user.update(msg)

    def update_balance(self, from_id, to_id, amount):
        self.balances[from_id][to_id] += amount
        self.balances[to_id][from_id] -= amount

    def add_expense(self, desc, amount, paid_by, users, split_type, values = None):
        split_factory = SplitFactory.split(split_type)
        splits = split_factory.calculate_split(amount, users, values)

        for split in splits:
            if split.user_id != paid_by:
                self.update_balance(paid_by, split.user_id, split.amount)

        self.notify(f"New expense: {desc} (Rs {amount})")

    def show_balances(self):
        print(f"\n=== Balances in {self.group_name} ===")
        for u in self.balances:
            for v, amt in self.balances[u].items():
                if amt > 0:
                    print(f"  {v} owes {amt:.2f}")
                else:
                    print(f"  owes {v}: {-amt:.2f}")

    def simplify(self):
        self.balances = DebtSimplifier.simplify(self.balances)


# ---------------- SINGLETON ----------------
class Splitwise:
    _instance = None

    def __init__(self):
        self.users = {}
        self.groups = {}

    @staticmethod
    def get_instance():
        if Splitwise._instance is None:
            Splitwise._instance = Splitwise()
        return Splitwise._instance

    def create_user(self, name, email):
        u = User(name, email)
        self.users[u.user_id] = u
        return u

    def create_group(self, name):
        g = Group(name)
        self.groups[g._id] = g
        return g


if __name__ == "__main__":
    manager = Splitwise.get_instance()

    u1 = manager.create_user("Aditya", "a@gmail.com")
    u2 = manager.create_user("Rohit", "r@gmail.com")
    u3 = manager.create_user("Manish", "m@gmail.com")

    g = manager.create_group("Trip")

    users = [u1.user_id, u2.user_id, u3.user_id]

    g.add_expense("Lunch", 900, u1.user_id, users, SplitType.EQUAL)
    g.show_balances()
    g.simplify()

    print("\nAfter simplification:")
    g.show_balances()
