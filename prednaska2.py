class Logger:

    _log_file = None

    def __new__(cls, filename):
        if not cls._log_file:
            cls._log_file = super().__new__(cls)
            cls._log_file.fp = open(filename, "a")
        return cls._log_file
    
    # def __init__(self, filename):
    #     self.fp = open(filename, "a")

    def add(self, message):
        self.fp.write(message + '\n')


if __name__ == "__main__":
    log1 = Logger("log1.txt")
    log2 = Logger("log2.txt")
    log3 = Logger("log3.txt")

    log1.add('zapis1')
    log2.add('zapis2')
    log3.add('zapis3')
            