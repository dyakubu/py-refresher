# Build a BankAccount class with:
# An initial balance of 0
# deposit(amount)
# withdraw(amount)
# get_balance()
# Concurrency setup:
# Create 10 threads
# 5 threads each deposit $100, 1,000 times
# 5 threads each withdraw $50, 1,000 times
# All threads operate on the same BankAccount instance
# The class must be thread-safe
# The lock should be owned by the BankAccount instance, not global

import threading 

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount 

    def withdraw(self, amount):
        with self.lock:
            if amount > self.balance:
                print("Withdrawal BLOCKED")
                return False
            self.balance -= amount 
            print("Withdrawal SUCCESSFUL")
            return True
        
def run_n_deposits(bankaccount, amount, freq):

    for _ in range(freq):
        bankaccount.deposit(amount)

def run_n_withdrawals(bankaccount, amount, freq):

    for _ in range(freq):
        bankaccount.withdraw(amount)

def main():

    b = BankAccount()
    tasks = []

    for i in range(10):
        if i % 2 == 0:
            tasks.append(threading.Thread(target=run_n_deposits, args=(b, 250, 1000)))
        else:
            tasks.append(threading.Thread(target=run_n_withdrawals, args=(b, 5000, 1000)))

    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    print(b.balance)



if __name__ == "__main__":
    main()