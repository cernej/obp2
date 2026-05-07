import os
import ast

if __name__ == "__main__":

    expr = input("Zadejte výraz: ")
    print(ast.literal_eval(expr))