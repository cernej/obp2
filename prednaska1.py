class NevalidniZustatek(Exception):
    pass

class Ucet:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.__zustatek = 0

    @property
    def zustatek(self):
        return self.__zustatek

    @zustatek.setter
    def zustatek(self, value):
        if value < 0:
            raise NevalidniZustatek("Zůstatek nemůže být záporný.")
        self.__zustatek = value

    def __str__(self):
        return f'Ucet {self.jmeno} zustatek: {self.zustatek} kc' 


if __name__ == '__main__':

    ucet1 = Ucet("bezny")
    ucet2 = Ucet("sporici")

    print(ucet1.zustatek)

    ucet1.zustatek = 1000

    print(ucet1.zustatek)
    print(ucet1)