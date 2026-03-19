from typing import Callable


def funkce1(value: str, y: int) -> int:
    print(f"{value} z funkce1")
    return 1


def funkce2(x: str, y: int) -> int:
    print(f"Dostal jsem parametr {x}")
    print("Ahoj z funkce2")
    return 2


def apply_function(func: Callable[[str, int], int]) -> None:
    print("Volam funkci:")
    vysledek = func("Cau", 1)
    print(f"Vysledek: {vysledek}")


if __name__ == '__main__':
    apply_function(funkce1)
    apply_function(funkce2)
    apply_function(lambda x, y: 0)
