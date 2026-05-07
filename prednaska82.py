
import asyncio
import time


class Callback:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, vysledek):
        with open(self.filename, "w") as f:
            f.write(f"Vysledek: {vysledek}\n")


def callbackfunction(vysledek):
    print(f"2. Vysledek je: {vysledek}")


async def spocitej(a, b, callback):
    vysledek = a + b
    print("2. Provádím dlouhou operaci...")
    await asyncio.sleep(5)  # Simulace dlouhé operace
    callback(vysledek)


async def dalsi_vypocty():
    print("1. Provadime dalsi vypocty...")
    await asyncio.sleep(2)
    print("1. Hotovo!")


async def main():
    a = 5
    b = 10

    await asyncio.gather(
        spocitej(a, b, Callback("vysledek.txt")),
        dalsi_vypocty(),
    )


if __name__ == "__main__":
    asyncio.run(main())


