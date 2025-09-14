# abstraction means hiding the implementation detail and only showing the essential feature to the user

class Car:
    def __init__(self):
        self.acc = False
        self.brk = False
        self.clutch = False

    def start(self):
        self.clutch = True
        self.acc = True
        print("The car is runnning...")

c1 = Car()
c1.start()