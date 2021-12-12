from typing import Optional
from enum import Enum, IntEnum
from oppapi import from_args, oppapi


class Food(Enum):
    A = "Apple"
    B = "Beer"
    C = "Chocolate"


class Price(IntEnum):
    A = 10
    B = 20
    C = 30


@oppapi
class Opt:
    food: Food
    price: Optional[Price]


def main():
    opt = from_args(Opt)
    print(opt)


# python simple.py 0.0.0.0 -p 8000
if __name__ == "__main__":
    main()
