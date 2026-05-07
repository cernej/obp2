class CounterIterator:
    def __init__(self, maximum):
        self.maximum = maximum
        self.current = 0

    def __next__(self):
        if self.current >= self.maximum:
            raise StopIteration
        self.current += 1
        return self.current

class Counter:
    def __init__(self, maximum):
        self.count = 0
        self.maximum = maximum

    def __iter__(self):
        return CounterIterator(self.maximum)
    

if __name__ == "__main__":
    counter = Counter(5)
    
    iter1 = iter(counter)
    iter2 = iter(counter)

    print(next(iter1))  # Output: 1
    print(next(iter1))  # Output: 2

    print(next(iter2))  # Output: 3

    print(next(iter1))  # Output: 4

    print(next(iter2))  # Output: 5