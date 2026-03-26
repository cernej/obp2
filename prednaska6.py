


def prvni():
    x = 10 / 0
    return x


def druha():
    a = prvni() + 1
    return a


def treti():
    try:
        y = druha() * 2
    except ZeroDivisionError as e:
        # print traceback
        import traceback
        traceback.print_exc()
        y = 0
    return y


def ctvrta():
    return treti() - 5



if __name__ == "__main__":

    print(ctvrta())
