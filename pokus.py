import ast


class A:
    def hello(self):
        print("Hello from class A!")
    
class B(A):
    def hello(self):
        print("Hello from class B!")

class C(A):
    def hello(self):
        print("Hello from class C!")

class D(B, C):
    pass


class User:
    #__slots__ = ["__role", "_initialized"]

    def __init__(self, role):
        self.__role = role
        self._initialized = False

    @property
    def role(self):
        return self.__role
    
    def __str__(self):
        return f"User(role={self.__role}, initialized={self._initialized})"


if __name__ == "__main__":

    # expr = input("Zadejte výraz: ")
    # value = ast.literal_eval(expr)
    # print(f"Vyhodnocená hodnota: {value}")

    d = D()
    d.hello()  # Která metoda hello() bude zavolána?
    print(D.__mro__)  # Zobrazí pořadí metod pro třídu D

    user = User("admin")
    user._initialized = True
    user._User__role = "user"
    user.__dict__["role"] = "guest"
    print(user.__dict__)
    print(user.role)

    def evil():
        print("Toto je zlovolná funkce!")
    setattr(user, "__str__", evil)
    print(user.__str__())