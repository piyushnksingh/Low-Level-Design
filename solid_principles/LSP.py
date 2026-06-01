# DEFINITION : SUBCLASS SHOULD BE SUBSTITUTABLE FOR THEIR BASE CLASS

# ------------------------------ LSP violated -------------------------------------

from abc import ABC, abstractmethod


class Account(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass


class SavingAccount(Account):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Savings Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Savings Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Savings Account!")


class CurrentAccount(Account):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Current Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Current Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Current Account!")


class FixedTermAccount(Account):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Fixed Term Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        raise Exception("Withdrawal not allowed in Fixed Term Account!")


class BankClient:
    def __init__(self, accounts):
        self.accounts = accounts

    def process_transactions(self):
        for acc in self.accounts:
            acc.deposit(1000)  # All accounts allow deposits

            # Assuming all accounts support withdrawal (LSP Violation)
            try:
                acc.withdraw(500)
            except Exception as e:
                print(f"Exception: {e}")


# Driver code
if __name__ == "__main__":
    accounts = [
        SavingAccount(),
        CurrentAccount(),
        FixedTermAccount()
    ]

    client = BankClient(accounts)
    client.process_transactions()




# ------------------------------ LSP followed -------------------------------------

from abc import ABC, abstractmethod


class DepositOnlyAccount(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass


class WithdrawableAccount(DepositOnlyAccount):
    @abstractmethod
    def withdraw(self, amount):
        pass


class SavingAccount(WithdrawableAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Savings Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Savings Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Savings Account!")


class CurrentAccount(WithdrawableAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Current Account. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrawn: {amount} from Current Account. New Balance: {self.balance}")
        else:
            print("Insufficient funds in Current Account!")


class FixedTermAccount(DepositOnlyAccount):
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount} in Fixed Term Account. New Balance: {self.balance}")


class BankClient:
    def __init__(self, withdrawable_accounts, deposit_only_accounts):
        self.withdrawable_accounts = withdrawable_accounts
        self.deposit_only_accounts = deposit_only_accounts

    def process_transactions(self):
        for acc in self.withdrawable_accounts:
            acc.deposit(1000)
            acc.withdraw(500)

        for acc in self.deposit_only_accounts:
            acc.deposit(5000)


# Driver code
if __name__ == "__main__":
    withdrawable_accounts = [
        SavingAccount(),
        CurrentAccount()
    ]

    deposit_only_accounts = [
        FixedTermAccount()
    ]

    client = BankClient(withdrawable_accounts, deposit_only_accounts)
    client.process_transactions()