import time


def yeild_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1


def return_up_to(n):
    result = []
    i = 1
    while i <= n:
        result.append(i)
        i += 1
    return result


if __name__ == "__main__":

    result = 0

    data = return_up_to(100000000)
    for number in data:
        result += number
    
    print(f'Výsledek: {result}')

    # for number in return_up_to(5000):
    #     print(number)

    time.sleep(30)