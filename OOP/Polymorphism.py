class Parent:
    def display(self):
        print("This is parent class")

    

class Child(Parent):
    def display(self):
         print("This is child class")
   

c1 = Child()
c1.display()

#here same method name i.e display is acting differently for different class