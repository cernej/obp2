class IterCisla:
    def __init__(self, max_cislo):
        self.__max_cislo = max_cislo
        self.__actual = 0

    def __next__(self):
        if self.__actual <= self.__max_cislo:
            actual = self.__actual
            self.__actual += 1
            return actual
        raise StopIteration


class Cisla:
    def __init__(self, max_cislo):
        self.max_cislo = max_cislo
    
    def __iter__(self):
        return IterCisla(self.max_cislo)


if __name__ == "__main__":

    cisla = Cisla(10)

    for i in cisla:
        print(i)

    iter1 = iter(cisla)
    iter2 = iter(cisla)

    print(next(iter1))
    print(next(iter1))
    print(next(iter2))
    print(next(iter1))
    print(next(iter1))
    print(next(iter2))
