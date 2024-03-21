# pylint: disable=missing-module-docstring,missing-function-docstring,eval-used
import sys


def main():
    """Implement the calculator"""
    first_number = int(sys.argv[1])
    operator = sys.argv[2]
    second_number = int(sys.argv[3])
    result = 0

    if operator == "+":
        result = first_number + second_number
    elif operator == "-":
        result = first_number - second_number
    elif operator == "*":
        result = first_number * second_number

    return result

if __name__ == "__main__":
    print(main())
