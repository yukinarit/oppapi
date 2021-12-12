from oppapi import field, from_args, oppapi
from typing import Optional


@oppapi
class Opt:
    foo: Optional[int] = field(metadata={"serde_rename": "bar"})
    """ Positional argument with `serde_rename` """


def main():
    opt = from_args(Opt)
    print(opt)


# python rename.py --bar 100
if __name__ == "__main__":
    main()
