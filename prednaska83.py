class Abc:

    def __init__(self, a, b):
        self.data = {"jmeno": "Alice", "vek": 30}

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        return None


if __name__ == "__main__":
    abc = Abc(1, 2)
    
    print(abc.jmeno)
    print(abc.vek)
    print(abc.zamestani)
    print(abc.praxe)


    print(dir(abc))