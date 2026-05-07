class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"User(name={self.name}, age={self.age})"


def evil():
    return "This is an evil function!"


if __name__ == "__main__":
    u = User("Alice", 30)

    setattr(u, "__str__", evil)
    setattr(u, "__repr__", evil)

    print(u.__str__())