
class Student:
    name = "Hari"

    @classmethod
    def ChangeName(cls, name):
        cls.name = name

s1 = Student()
s1.name = "Pukar"
print(s1.name)