#define a class Circle to create a circle with radius r using constructor.
#Define Area method which calculate the area 
#Define parameter method which calculate the parameter

class Circle:
    @staticmethod
    def Area(r):
        z=3.14*r*r
        return z
       
    @staticmethod
    def perimeter(r):
         z = 2*3.14*r
         return z

c1 = Circle()
result = c1.Area(4)
print(result)

result2 = c1.perimeter(4)
print(result2)

