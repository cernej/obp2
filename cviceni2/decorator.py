# pridejte dekorator @log, ktery vypise, ktera funkce se vola (kazda funkce ma sve jmeno v atributu __name__)

def funkce1():
    print("Funkce 1")

def funkce2():
    print("Funkce 2")



if __name__ == "__main__":
    funkce1()
    funkce2()