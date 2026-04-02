from contextlib import contextmanager


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print('Vstupuju do kontextu')
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Opouštím kontext')
        self.file.close()


@contextmanager
def file_handler(filename):
    print('Vstupuju do kontextu')
    f = open(filename, "r")
    try:
        yield f
    finally:
        f.close()
    print('Opouštím kontext')


if __name__ == "__main__":

    with FileHandler("data.txt") as f:
        print('Ctu soubor')
        data = f.read()
        print(data)
    print('Jsem mimo kontext')

    with file_handler("data.txt") as f:
        print('Ctu soubor')
        data = f.read()
        print(data)
    print('Jsem mimo kontext')