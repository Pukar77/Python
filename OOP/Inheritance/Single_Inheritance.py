
class Car:
    @staticmethod
    def start():
        print("Car is starting...")
    
    @staticmethod
    def stop():
        print("The car is stopping...")

class bike(Car):
    @staticmethod
    def cornering():
        print("The bike is performing cornering")

b1 = bike()
b1.cornering()
b1.start()
b1.stop()