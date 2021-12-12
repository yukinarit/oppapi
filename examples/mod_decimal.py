from oppapi import oppapi, from_args
from decimal import Decimal


@oppapi
class Opt:
    value: Decimal


def main():
    opt = from_args(Opt)
    print(opt)


if __name__ == "__main__":
    main()
