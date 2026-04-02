import time
from contextlib import contextmanager

@contextmanager
def log_time():
    import time
    start_time = time.time()
    print('Začínám měřit čas')
    yield
    end_time = time.time()
    print(f'Čas měření: {end_time - start_time} sekund')


if __name__ == "__main__":

    with log_time():
        result = 0
        for i in range(10000000):
            result += i
    print(f'Výsledek: {result}')

    time.sleep(20)