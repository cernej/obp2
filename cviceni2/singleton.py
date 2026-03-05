# vytvorte singleton, ktery loguje do souboru

class Logger:

    _instance = None

    def __new__(cls, log_file):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._log_file = log_file
        return cls._instance

    # def __init__(self, log_file=None):
    #     self._log_file = log_file

    def log(self, message):
        with open(self._log_file, "a") as f:
            print(f"zapisuji do souboru {self._log_file}: {message}")
            f.write(message + "\n")


if __name__ == "__main__":
    logger1 = Logger("log1.txt")
    logger2 = Logger("log2.txt")
    logger3 = Logger("log3.txt")

    logger1.log("Hello from logger1")
    logger2.log("Hello from logger2")
    logger3.log("Hello from logger3")
