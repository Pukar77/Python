class Student:
    def __init__(self,name, roll):
        self.name = name
        self.roll = roll
    
    def display(self):
        print(f"Hey this student name is {self.name} and this student roll number is {self.roll}")

        print("hey, we can also print as", self.name)

s1 = Student("Pukar", 20)
s2 = Student("Rimal", 21)

s1.display()
s2.display()
        