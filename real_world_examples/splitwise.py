from abc import ABC, abstractmethod
from collections import defaultdict


# ------------------ Split + Types ------------------
class Split:
    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount

class SplitType:
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"


# ------------------ Strategy ------------------
class SplitStrategy(ABC):
    @abstractmethod
    def calculate_split(self, total, user_ids, values = None): # default None for equal split
        pass

class EqualSplit(SplitStrategy):
    def calculate_split(self, total, user_ids, values=None):
        amount = total / len(user_ids)
        return [Split(user_id, amount) for user_id in user_ids]

class ExactSplit(SplitStrategy):
    def calculate_split(self, total, user_ids, values=None):
        return [Split(user_ids[i], values[i]) for i in range(len(user_ids))]

class PercentageSplit(SplitStrategy):
    def calculate_split(self, total, user_ids, values=None):
        return [Split(user_ids[i], total * values[i] / 100) for i in range(len(user_ids))]


# ---------------- FACTORY ----------------
class SplitFactory:
    @staticmethod
    def get_split(split_strategy: SplitStrategy):
        if split_strategy == SplitType.EXACT:
            return ExactSplit()
        elif split_strategy == SplitType.PERCENTAGE:
            return PercentageSplit()
        else:
            return EqualSplit() # default to Equal split

# ------------------ Observer ------------------
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# ---------------- USER ----------------
class User(Observer):
    _id = 0
    def __init__(self, user_name, email):
        User._id += 1
        self.user_id = f"user_{User._id}"
        self.user_name = user_name
        self.email = email
        self.balances = defaultdict(float) # map

    def update(self, msg):
        print(f"[NOTIFICATION to {self.user_name}]: {msg}")

    def update_balance(self, amount, other):
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
        self.expense_id = f"expense_{Expense._id}"
        self.desc = desc
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits
        self.group_id = group_id

# ---------------- DEBT SIMPLIFIER ----------------
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
            elif amt < 0:
                debitors.append([u, -amt]) # NOTE : amt inserted as +ve

        creditors.sort(key = lambda x: -x[1]) # sort in descending order
        debitors.sort(key = lambda x: -x[1]) # sort in descending order

        result = {u : {} for u in group_balances}

        i = j = 0
        while i < len(creditors) and j < len(debitors):
            c_id, c_amt = creditors[i]
            d_id, d_amt = debitors[j]

            settle = min(c_amt, d_amt)

            result[c_id][d_id] = settle
            result [d_id][c_id] = -settle

            creditors[i][1] -= settle
            debitors[j][1] -= settle

            if creditors[i][1] < 0.01:
                i+=1
            if debitors[j][1] < 0.01:
                j+=1

        return result

# ------------------ Group ------------------
class Group:
    _id = 0
    def __init__(self, name):
        Group._id += 1
        self.group_id = f"group_{Group._id}"
        self.group_name = name
        self.members = []
        self.balances = defaultdict(lambda: defaultdict(float)) # to store user_id wise all the user_ids and amounts which
                                                                # the user_ids need to pay or get from user_id

    def add_member(self, user):
        self.members.append(user)

    def delete_member(self, user):
        self.members.remove(user)

    def notify(self, msg):
        for member in self.members:
            member.update(msg)

    def update_balance(self, from_id, to_id, amount):
        self.balances[from_id][to_id] += amount
        self.balances[to_id][from_id] -= amount

    def add_expense(self, desc, amount, paid_by, users, split_type, values = None):
        split_factory = SplitFactory.get_split(split_type)
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
        self.groups[g.group_id] = g
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