import re


if __name__ == "__main__":

    text = "Toto je nějaký text s emailem: vkobzev@jcu.cz a speciálními znaky !@#."

    text = re.sub(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "XXX", text)

    print(text)

    # if not re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
    #     print("email je nevalidni")
    # else:
    #     print(f"validni email '{email}'")