from abc import ABC, abstractmethod

class MetodaNeniImplementovana(Exception):
    pass


def abstractmethod_decorator(func):
    def wrapper(*args, **kwargs):
        raise MetodaNeniImplementovana("Metoda musi byt implementovana")
    return wrapper


class AbstractClass:
    @abstractmethod_decorator
    def method(self):
        pass

class MyClass(AbstractClass):
    def method(self):
        print("Implementace metody")



if __name__ == "__main__":
    my_object = MyClass()
    my_object.method()
