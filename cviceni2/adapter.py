
class OldPrinter:
    def print_text(self, text):
        print(text)


class Printer:
    def print(self, message):
        ...
 

if __name__ == "__main__":
    printer = Printer()
    printer.print("Hello, World!")