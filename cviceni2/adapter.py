
class OldPrinter:
    def print_text(self, text):
        print(f"Tisku na stare tiskarne: {text}")


class Printer:
    def print(self, message):
        print(f"Tisku na nove tiskarne: {message}")
 

class Adapter(Printer):
    def __init__(self):
        self.old_printer = OldPrinter()
    
    def print(self, message):
        self.old_printer.print_text(message)


if __name__ == "__main__":
    printer = Printer()
    printer.print("Hello, World!")

    adapter_na_starou_tiskarnu = Adapter()
    adapter_na_starou_tiskarnu.print("Hello, World!")