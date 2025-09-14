# Methods which donot use self parameters are static method


class Bikers:
    @staticmethod
    def display():
        print("Hey this is static method, if we donot write @staticmethod then it will throw an error")

b = Bikers()
b.display()