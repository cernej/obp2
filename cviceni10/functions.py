import random
import datetime
import requests


def neg(x):
    if x < 20 and x > -20:
        return -x
    return x


def rev(items):
    return list(reversed(items))


def rnd(x):
    return random.randint(0, x)


def greet(name):
    now = datetime.datetime.now()
    if now.hour < 12:
        return f"Good morning, {name}!"
    elif now.hour < 18:
        return f"Good afternoon, {name}!"
    else:
        return f"Good evening, {name}!"


class DownloadError(Exception):
    pass


def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise DownloadError(f"Failed to download data from {url}. Status code: {response.status_code}")



if __name__ == "__main__":
    print(rnd(10))
    print(greet("Alice"))
    try:
        data = download("https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt")
        print(data[:100])  # Print the first 100 characters of the downloaded data
    except DownloadError as e:
        print(e)