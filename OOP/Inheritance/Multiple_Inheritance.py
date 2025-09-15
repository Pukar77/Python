class Base1:
    @staticmethod
    def display():
        print("This is first base class")

class Base2:
    @staticmethod
    def show():
        print("This is second base class")


class Child(Base1, Base2):
    @staticmethod
    def printing():
        print("This is child method")

c1 = Child()
c1.printing()
c1.show()
c1.display()