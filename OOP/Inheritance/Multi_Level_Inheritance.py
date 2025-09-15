class bike:
    @staticmethod
    def start():
        print("Bike is starting")

    @staticmethod
    def stop():
        print("Bike is stopping")

class dirt(bike):
    @staticmethod
    def offroad():
        print("This bike can run smoothly in offroad")

class xpulse(dirt):
    @staticmethod
    def bestbike():
        print("Xpulse is the best offroad bike")

x = xpulse()
x.bestbike()
x.offroad()
x.start()
x.stop()
