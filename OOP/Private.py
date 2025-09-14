# Private methods or attributes are those methods or attribute that cannot be accessed outside the class, OR in simple terms we can say that, the scope of the attribute or method is only within the class

class Account:
    def __init__(self, accname, accpass):
        self.accname = accname
        self.__accpass = accpass   #private attribute

a1 = Account("Pukar", "123")

#Throes error since it is trying to access the private attrbiute outside the class
print(a1.__accpass)