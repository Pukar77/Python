#Create student class that takes names and marks for 3 students through constructors and create a method to display the average of marks

class Student:

    def __init__(self, name, marks1,marks2, marks3):
        self.name = name
        self.marks1 = marks1
        self.marks2 = marks2
        self.marks3 = marks3

    def average(self):
        average = (self.marks1+self.marks2+self.marks3)/3
        print("Average of the 3 marks is ", average)

s1= Student("Pukar", 99,98,97)


s1.average()






        