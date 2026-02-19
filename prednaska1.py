class NevalidniVklad(Exception):
    pass

class Ucet:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.__zustatek = 0
    
    @property
    def zustatek(self):
        return self.__zustatek

    def vloz(self, castka):
        if castka <= 0:
            raise NevalidniVklad(f'Vkladana castka {castka} je mensi nebo rovna 0')
        self.__zustatek += castka

    def __str__(self):
        return f'Ucet {self.jmeno} zustatek: {self.zustatek} kc' 


if __name__ == '__main__':

    ucet1 = Ucet("bezny")
    ucet2 = Ucet("sporici")

    print(ucet1)
    print(ucet2)

    ucet1.vloz(100)
    print(ucet1)

    ucet2.vloz(100)
    print(ucet2)