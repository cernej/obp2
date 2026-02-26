# vytvorte singleton, ktery loguje do souboru

class Logger:

    def __init__(self, log_file=None):
        self._log_file = log_file

    def log(self, message):
        with open(self._log_file, "a") as f:
            print(f"zapisuji do souboru {self._log_file}: {message}")
            f.write(message + "\n")


if __name__ == "__main__":
    logger1 = Logger("log1.txt")
    logger2 = Logger("log2.txt")

    logger1.log("Hello from logger1")
    logger2.log("Hello from logger2")