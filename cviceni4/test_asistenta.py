from asistent import Vyzkumnik, Kritik, Korektor

# API_KEY ziskate na https://aistudio.google.com/

if __name__ == "__main__":
    vyzkumnik = Vyzkumnik("API_KEY")
    kritik = Kritik("API_KEY")
    korektor = Korektor("API_KEY")
    
    zadani = "Jak nejsnadneji dostudovat EF JCU?"

    odpoved = vyzkumnik.generate_content(zadani)

    print(odpoved)

    kritika = kritik.generate_content(odpoved)

    print(kritika)

    vysledek = korektor.generate_content(odpoved + "\n" + kritika)

    print(vysledek)
