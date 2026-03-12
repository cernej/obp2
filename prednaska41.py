import random
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int
    _id: int = field(init=False, compare=False)

    def __post_init__(self):
        self._id = random.randint(1, 1000000)


class User2:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__post_init__()
    
    def __post_init__(self):
        self._id = random.randint(1, 1000000)
    
    def __repr__(self):
        return f"User2()..."
    
    def __eq__(self, value):
        return self.name == value.name and self.age == value.age


if __name__ == "__main__":
    u1 = User("Alice", 18)
    u2 = User("Bob", 18)
    u3 = User("Alice", 18)
    print(u1)