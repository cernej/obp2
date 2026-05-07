if __name__ == "__main__":
    
    jmena = ["Alice", "Bob", "Charlie", "David", "Eve"]
    veky = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

    for jmeno, vek in zip(jmena, veky):
        print(f"{jmeno} je {vek} let starý.")