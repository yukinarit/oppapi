from typing import List, Tuple, Optional
from oppapi import from_args, oppapi


@oppapi
class Opt:
    values: List[int]
    opts: Optional[Tuple[int, str, float, bool]]


def main():
    opt = from_args(Opt)
    print(opt)


# python nargs.py 1 2 3 --opts 10 foo 10.0 True
if __name__ == "__main__":
    main()
