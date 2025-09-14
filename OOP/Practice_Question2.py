# create a class Account having 2 attribute - balance and acc no
# create methods for debit, credit and printing the balance


class Account:
    def __init__(self, balance, accno):
        self.balance = balance
        self.accno = accno

    def debit(self, addedamount):
        self.balance += addedamount
    
    def credit(self, subamount):
        self.balance -= subamount

    def display(self):
        print(f"The balance of Acc no {self.accno} is {self.balance}")


a1 = Account(20, 1234567)
a1.debit(10)
a1.credit(15)
a1.display()
