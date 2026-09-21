# ENCAPSULATION:
# Bundle data + methods that operate on that data inside a class.
# Control how the internal data can be accessed/modified.
#
# __balance is private/internal state.
# User cannot directly modify it through the intended interface.
#
# deposit() and withdraw() control how balance changes.
# get_balance() provides controlled access to the balance.
#
# Abstraction vs Encapsulation:
#
# Abstraction:
#   Hides HOW something works.
#   Example: payment.pay() hides payment processing details.
#
# Encapsulation:
#   Protects and controls access to DATA.
#   Example: __balance can only be changed through deposit/withdraw.
#
# Python:
#   __balance -> name mangling, commonly used for private attributes.
#   _balance  -> convention for "internal/protected" usage, not truly private.

# One subtle interview point
# Don't say:
# "__balance is completely inaccessible from outside."
# That's not technically true in Python because of name mangling. Python doesn't enforce private access as strictly as languages like Java/C++.
#
# Say:
# "__balance is intended to be private, and Python uses name mangling to discourage direct external access."

class BankAccount:
    def __init__(self):
        self.__balance = 0

    def deposit(self, amount: int):
        if amount <= 0:
            return
        self.__balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            return

        if amount > self.__balance:
            print("Not enough money..")
        else:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance


def main():
    bank = BankAccount()

    bank.deposit(100)
    bank.withdraw(200)
    print(bank.get_balance())

    bank.deposit(100)
    bank.withdraw(200)
    print(bank.get_balance())

if __name__ == "__main__":
    main()



