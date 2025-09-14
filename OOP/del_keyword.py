# Del keyword is used to delete the object property or object itself

class Student:
    def __init__(self, name):
        self.username = name
    
s1 = Student("Pukar")
print("Successfully deleted the item")
del s1.username