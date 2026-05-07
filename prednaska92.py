class Pokus:
    def __init__(self, polozky=None):
        if polozky is None:
            self.polozky = []
        else:
            self.polozky = polozky
    
    def pridej(self, polozka):
        self.polozky.append(polozka)
    
    def __str__(self):
        return f"Pokus(polozky={self.polozky})"


if __name__ == "__main__":
    p1 = Pokus()
    p2 = Pokus()

    p1.pridej("prvni")
    p1.pridej("druhy")

    p2.pridej("treti")

    print(p1)
    print(p2)

