from typing import Optional, Union
from oppapi import from_args, oppapi
import logging
logging.basicConfig(level=logging.INFO)


@oppapi
class Foo:
    a: int


@oppapi
class Bar:
    a: str
    b: Optional[int]


@oppapi
class Opt:
    sub: Union[Foo, Bar]


def main():
    opt = from_args(Opt)
    print(opt, isinstance(opt.sub, Foo))


# python simple.py 0.0.0.0 -p 8000
if __name__ == "__main__":
    main()
